from django.urls import path
from . import views

urlpatterns = [
    path('about_events/',views.about_events,name="about_events"),
    path('art_landing/',views.art_landing,name="art_landing"),
    path('art_gallery/',views.art_gallery,name="art_gallery"),
    path('contact_us/',views.contact_us,name="contact_us"),
    path('art_contact/',views.art_contact,name="art_contact"),
    path('about_us/',views.about_us,name="about_us"),
    path('comming_soon/',views.comming_soon,name="comming_soon"),
    path('',views.index,name="index"),
    path('terms_and_conditions/',views.terms_and_conditions,name="terms_and_conditions"),
    path('privacy_policy/',views.privacy_policy,name="privacy_policy"),
     path('working_on/',views.working_on,name="working_on")
]