from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payments/gd/enroll/<slug:slug>/', views.enroll_in_groupdiscussion, name='enroll_in_groupdiscussion'),
    path('payments/gd/success/<slug:slug>/', views.payments_for_group_discussion, name='payment_for_group_discussion'),
    path("payments/dashboard/", views.dashboard, name="dashboard"),
    path("payments/pricing/", views.pricing, name="pricing"),
    path("payments/free-booking/<slug:slug>/", views.book_free_service, name="free_booking"),
]