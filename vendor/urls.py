from django.urls import path
from . import views

urlpatterns = [
    path('vendor_dashboard/',views.vendor_dashboard,name="vendor_dashboard"),
    path('edit_vendor_profile/',views.edit_vendor_profile,name="edit_vendor_profile"),
    path('vendor_change_password/',views.vendor_change_password,name="vendor_change_password")
]