from django.shortcuts import render

# Create your views here.


def about_events(request):
    return render(request,'about_events.html')


def art_landing(request):
    return render(request,'art_landing.html')


def art_gallery(request):
    return render(request,'art_gallery.html')


def contact_us(request):
    return render(request,'contact_us.html')

def art_contact(request):
    return render(request,'art_contact.html')


def about_us(request):
    return render(request,'about_us.html')