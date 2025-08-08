from django.urls import path
from . import views

urlpatterns = [
    path('about_events/',views.about_events,name="about_events"),
    path('art_landing/',views.art_landing,name="art_landing"),
    path('art_gallery/',views.art_gallery,name="art_gallery"),
    path('contact_us/',views.contact_us,name="contact_us"),
    path('art_contact/',views.art_contact,name="art_contact"),
    path('about_us/',views.about_us,name="about_us"),
    path('',views.index,name="index")
]