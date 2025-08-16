from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_otp/<int:user_id>/',views.verify_otp,name="verify_otp"),
    path('select_category/',views.select_category,name="select_category"),
    path('participant_basic_details/',views.participant_basic_details,name="participant_basic_details"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('mentor_register/',views.mentor_register,name="mentor_register"),
    path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),
]