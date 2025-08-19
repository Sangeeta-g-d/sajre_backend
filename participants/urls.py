from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name="dashboard"),
    path('terms/',views.terms,name="terms"),
    path('profile/',views.profile,name="profile"),
    path("update-photo/", views.update_profile_photo, name="update_profile_photo"),
    path('change_password/',views.change_password,name="change_password"),
    path("update-terms-status/", views.update_terms_status, name="update_terms_status"),
    path("create-order/", views.create_razorpay_order, name="create_razorpay_order"),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment_failed',views.payment_failed,name="payment-failed"),
    path('p_working_on/',views.p_working_on,name="p_working_on")

]