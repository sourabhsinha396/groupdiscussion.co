from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out

from .forms import SignupForm, LoginForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print("request.POST ", request.POST)
        if form.is_valid():
            user = form.save()
            
            user.backend = "apps.authentication.backends.EmailOrUsernameModelBackend"
            login(request, user)
            messages.success(request, "You have successfully Logged In")

            next_url = request.session.get("next", "/")
            if request.session.get("next"):
                del request.session["next"]
            return redirect(next_url)
        else:
            messages.error(request, form.errors)
    else:
        form = SignupForm()
    context = {"form": form, "domain": settings.BASE_DOMAIN_URL}
    return render(request, "authentication/signup.html", context=context)


def login_user(request):
    next_url = request.GET.get("next", "/")
    request.session["next"] = next_url
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "You have successfully Logged In")
            
            if request.session.get("next"):
                del request.session["next"]
            return redirect(next_url)
        else:
            messages.error(request, form.errors)
            context = {"form": form, "domain": settings.BASE_DOMAIN_URL}
            return render(request, "authentication/login.html", context=context)
    form = LoginForm()
    context = {"form": form, "domain": settings.BASE_DOMAIN_URL}
    return render(request, "authentication/login.html", context=context)


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    messages.success(request,'You have successfully logged out.')


def password_reset_request_sent(request):
    """Displays a message that says, password reset mail has been sent."""
    return render(request, 'authentication/password_reset_request_sent.html')


def password_reset_complete(request):
    messages.success(request, 'Your password has been reset successfully. Kindly Login Now.')
    return redirect("common:home")
