from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("authentication/forgot-password/", auth_views.PasswordResetView.as_view(template_name="authentication/forgot_password.html"), name="forgot_password"),
    path("authentication/reset-request-sent", views.password_reset_request_sent, name="password_reset_done"),
    path("authentication/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="authentication/choose_new_password.html"), name="password_reset_confirm"),
    path("authentication/reset/complete/", views.password_reset_complete, name="password_reset_complete"),
]