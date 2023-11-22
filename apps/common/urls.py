from django.urls import path
from . import views

app_name = "common"

urlpatterns = [
    path("", views.home, name="home"),
    path("contactus/", views.contact_us, name="contact_us"),
    path("aboutus/", views.about_us, name="about_us"),
    path("terms/", views.terms_and_conditions, name="terms_and_conditions"),
    path("privacy/", views.privacy_policy, name="privacy_policy"),
    path("refund-policy/", views.refund_policy, name="refund_policy"),
]