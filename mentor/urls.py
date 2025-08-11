from django.urls import path
from . import views

urlpatterns = [
    path('mentor_dashboard/',views.mentor_dashboard,name="mentor_dashboard"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('mentor_change_password/',views.mentor_change_password,name="mentor_change_password")
]