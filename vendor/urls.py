from django.urls import path
from . import views

urlpatterns = [
    path('vendor_dashboard/',views.vendor_dashboard,name="vendor_dashboard"),
    path('edit_vendor_profile/',views.edit_vendor_profile,name="edit_vendor_profile"),
    path('vendor_change_password/',views.vendor_change_password,name="vendor_change_password"),
    path('v_terms/',views.v_terms,name="v_terms"),
    path('v_working_on/',views.v_working_on,name="v_working_on"),
    path('create_vendor_profile/',views.create_vendor_profile,name="create_vendor_profile"),
    path('mentor_list/',views.mentor_list,name="mentor_list"),
]