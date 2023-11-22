from django.shortcuts import render
from django.contrib import messages

from .forms import ContactUsForm


def home(request):
    return render(request, 'common/home.html')


def about_us(request):
    return render(request, 'common/about_us.html')


def terms_and_conditions(request):
    return render(request, 'common/terms_and_conditions.html')


def privacy_policy(request):
    return render(request, 'common/privacy_policy.html')


def refund_policy(request):
    return render(request, 'common/refund_policy.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully.')
        else:
            messages.error(request, 'Please correct the errors below.')
            messages.error(request, form.errors)
    else:
        form = ContactUsForm()
    return render(request, 'common/contact_us.html', {'form': form})