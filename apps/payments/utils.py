from django.contrib import messages
from django.contrib.auth.models import User

from .models import CouponCode, Payment, Referral, Credit


def get_actual_payment_amount(amount)->int:
    return int(amount)//100


def get_discounted_amount(price,code,request)->int:
    razorpay_conversion_factor = 100
    if code:
        coupon_code = CouponCode.objects.filter(code=code)
        if coupon_code.exists():
            discount = coupon_code.last().discount
            messages.success(request,f"Successfully applied a discount of {discount}%")
            discounted_amount = price - ((price*discount)/100)
            return discounted_amount * razorpay_conversion_factor
        messages.error(request,f"Oops, looks like this coupon code is no longer valid!")
    return price * razorpay_conversion_factor


def multiplier(amount, razorpay_multiplier=100):
    return amount * razorpay_multiplier


def set_referer(referer, payment:Payment):
    referer = referer
    if referer:
        try:
            user = User.objects.get(username=referer)
        except User.DoesNotExist:
            print("User does not exist to set referer")
            return None
        referral = Referral.objects.create(payment=payment,referer=user)
        return referral
    return None


def add_referral_credits(referer, payment:Payment):
    referer = referer
    if referer:
        try:
            user = User.objects.get(username=referer)
        except User.DoesNotExist:
            print("User does not exist to add referral credits")
            return None
        commision_denominator = 3
        if user.credits.exists():
            credit = user.credits.first()
            credit.amount += get_actual_payment_amount(payment.amount)//commision_denominator
            credit.payment = payment
            credit.save()
            return credit
        
        credits = Credit.objects.create(user=user,amount=get_actual_payment_amount(payment.amount)//commision_denominator,reason="Referral Credits",payment=payment)
        return credits
    return None
        

def deduct_referral_credits(user, amount):
    credit = Credit.objects.filter(user=user).first()
    if credit:
        credit.amount -= amount
        credit.save()
        return credit