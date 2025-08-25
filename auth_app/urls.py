from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_otp/<int:user_id>/', views.verify_otp, name="verify_otp"),
    path('select_category/', views.select_category, name="select_category"),
    path('participant_basic_details/', views.participant_basic_details, name="participant_basic_details"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('complete_profile/', views.mentor_register, name='mentor_register'),
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),

    # ---- Forgot / Reset Password ----
    path('forgot_password/', views.forgot_password, name='forgot_password'),

    path('send-reset-link/', 
         auth_views.PasswordResetView.as_view(
             template_name='forgot_password.html',
             email_template_name='password_reset_email.html',
             success_url='/auth/reset-link-sent/'
         ), 
         name='send_reset_link'),

    path('reset-link-sent/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='reset_link_sent.html'
         ), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='reset_password_form.html'
         ), 
         name='password_reset_confirm'),

    path('reset-password-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='reset_password_complete.html'
         ), 
         name='password_reset_complete'),
]
