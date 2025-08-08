from django.urls import path
from . import views

urlpatterns = [
    path('mentor_dashboard/',views.mentor_dashboard,name="mentor_dashboard")
]