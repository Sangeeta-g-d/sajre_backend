from django.shortcuts import render

# Create your views here.


def mentor_dashboard(request):
    return render(request,'mentor_dashboard.html')