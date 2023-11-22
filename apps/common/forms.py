from django import forms
from .models import ContactUs
from django_recaptcha.fields import ReCaptchaField


class ContactUsForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'message', 'captcha']