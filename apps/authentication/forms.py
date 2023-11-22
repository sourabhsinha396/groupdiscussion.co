import random
from django_recaptcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('name', 'first_name', 'last_name', 'email', 'password1', 'password2', 'captcha')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the 'name' field to the form
        self.fields['name'] = forms.CharField(max_length=100, required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is already taken")
        return email

    def clean_username(self):
        """create a unique username from the name entered by the user"""
        name = self.cleaned_data.get('name')
        username = name.replace(" ", "").lower()
        qs = User.objects.filter(username=username)
        if qs.exists():
            username = username + str(random.randint(1, 1000))
        return username

    def clean_first_name(self):
        """clean the first name entered by the user"""
        name = self.cleaned_data.get('name')
        first_name = name.split(" ")[0]
        return first_name

    def clean_last_name(self):
        """clean the last name entered by the user"""
        last_name = ""
        name = self.cleaned_data.get('name')
        if len(name.split(" ")) > 1:
            last_name = name.split(" ")[-1]
        return last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.clean_username()
        user.is_active = True
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        return cleaned_data