import requests
import razorpay

from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .utils import get_discounted_amount
from .utils import set_referer, add_referral_credits
from .models import PaymentAttempt, Payment
from apps.groupdiscussions.models import GroupDiscussion

if settings.DEBUG:
    razorpay_key = settings.RAZORPAY_TEST_KEY
    razorpay_secret = settings.RAZORPAY_TEST_SECRET_KEY
else:
    razorpay_key = settings.RAZORPAY_LIVE_KEY
    razorpay_secret = settings.RAZORPAY_LIVE_SECRET_KEY

def track_payment_attempt(user, group_discussion, message="attempted"):
    payment_attempt = PaymentAttempt.objects.filter(user=user,group_discussion=group_discussion).first()
    if payment_attempt:
        payment_attempt.updated_at = timezone.now()
        payment_attempt.message = message
        payment_attempt.save()
    else:
        PaymentAttempt.objects.create(user=user,group_discussion=group_discussion,message=message)


@login_required
def enroll_in_groupdiscussion(request, slug):
    group_discussion = GroupDiscussion.objects.get(slug=slug)
    if group_discussion.is_free:
        return redirect('payments:free_booking', slug=slug)
    
    coupon_code = request.GET.get("code")
    amount = get_discounted_amount(price=group_discussion.price,code=coupon_code,request=request)
    client = razorpay.Client(auth=(razorpay_key, razorpay_secret))
    currency = "INR"
    response = client.order.create({'amount':int(amount),'currency':currency,'payment_capture':1,
                                    "notes":{'gd_title':group_discussion.title,'user_email':request.user.email, "coupon_code":coupon_code,
                                             "referer": request.session.get('referer', None)}})
    
    track_payment_attempt(user=request.user,group_discussion=group_discussion)
    context = {'response':response,'group_discussion':group_discussion,"razorpay_client_key":razorpay_key,'amount':int(amount)/100}
    return render(request, 'payments/initialization.html', context=context)


@csrf_exempt
def payments_for_group_discussion(request, slug):
    group_discussion = GroupDiscussion.objects.get(slug=slug)

    if request.method == "GET":
        payment = Payment.objects.filter(payee=request.user,group_discussion=group_discussion).first()
        context = {'payment':payment}
        return render(request, 'payments/payment_status.html', context=context)
    
    if request.method == "POST":
        client = razorpay.Client(auth=(razorpay_key, razorpay_secret))
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_payment = client.payment.fetch(razorpay_payment_id)

        user_email = razorpay_payment['notes'].get('user_email', None)
        payee = User.objects.get(email=user_email)
        coupon_code = razorpay_payment['notes'].get('coupon_code', None)
        
        status = "paid" if razorpay_payment['status'] == 'captured' else "failed"
        payment = Payment.objects.create(mentor=group_discussion.mentor,payee=payee,group_discussion=group_discussion,
                                         amount=razorpay_payment['amount'],currency=razorpay_payment['currency'],
                                         status=status,order_id=razorpay_payment['order_id'],
                                         payment_id=razorpay_payment['id'],
                                         coupon=coupon_code,
                                         extra=razorpay_payment)
        track_payment_attempt(user=payee,group_discussion=group_discussion,message=status)

        referer = razorpay_payment['notes'].get('referer', None)
        set_referer(referer=referer, payment=payment)
        add_referral_credits(referer=referer, payment=payment)
        requests.post("https://ntfy.sh/fastapi", data=f"New Booking for GroupDiscussion.Co {user_email}.".encode(encoding='utf-8'))
        context = {'payment':payment}
        return render(request, 'payments/payment_status.html', context=context)


@login_required
def dashboard(request):
    payments = Payment.objects.filter(payee=request.user)
    context = {'payments':payments}
    return render(request, 'payments/dashboard.html', context=context)


def pricing(request):
    return redirect('groupdiscussions:list_group_discussions')


@login_required
def book_free_service(request, slug: str):
    group_discussion = GroupDiscussion.objects.get(slug=slug)
    payment = Payment.objects.create(mentor=group_discussion.mentor,payee=request.user,group_discussion=group_discussion,
                                     amount=0,currency='INR',status="paid",order_id="free",
                                     payment_id="free",coupon=None,extra={})
    requests.post("https://ntfy.sh/fastapi", data=f"New Free Booking for GroupDiscussion.Co {request.user.email}.".encode(encoding='utf-8'))
    context = {'payment':payment}
    return render(request, 'payments/payment_status.html', context=context)