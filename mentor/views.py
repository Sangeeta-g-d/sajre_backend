from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from auth_app.models import CustomUser
from admin_part.models import Participant,CompetitionCategory
from django.contrib.auth import update_session_auth_hash
# Create your views here.

@login_required
def mentor_dashboard(request):
    # Count mentors referred by this user
    referred_mentors_count = CustomUser.objects.filter(
        referred_by=request.user,
        role="mentor"
    ).count()

    # ✅ If mentor has referred 5 or more mentors → change role to vendor
    if referred_mentors_count >= 5 and request.user.role == "mentor":
        request.user.role = "vendor"
        request.user.save(update_fields=["role"])

    # Count students (participants) referred by this user
    referred_students_count = CustomUser.objects.filter(
        referred_by=request.user,
        role="participant"
    ).count()

    # Count enrolled students (participants who have paid)
    enrolled_students_count = Participant.objects.filter(
        user__referred_by=request.user,
        has_paid=True
    ).count()

    # Get category-wise data for pie charts
    categories = CompetitionCategory.objects.all()
    category_data = []
    
    for category in categories:
        total = CustomUser.objects.filter(
            referred_by=request.user,
            role="participant",
            participant__category=category
        ).count()
        
        enrolled = Participant.objects.filter(
            user__referred_by=request.user,
            category=category,
            has_paid=True
        ).count()
        
        category_data.append({
            'name': category.name,
            'total': total,
            'enrolled': enrolled,
            'not_enrolled': total - enrolled if total > enrolled else 0
        })

    return render(request, 'mentor_dashboard.html', {
        'referred_mentors_count': referred_mentors_count,
        'referred_students_count': referred_students_count,
        'enrolled_students_count': enrolled_students_count,
        'category_data': category_data,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import json

@login_required
def edit_profile(request):
    user = request.user
    mentor_profile = user.mentor_profile
    
    if request.method == 'POST':
        try:
            # Update User fields
            user.full_name = request.POST.get('full_name', user.full_name)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            user.save()
            
            # Update MentorProfile fields
            mentor_profile.higher_qualification = request.POST.get('higher_qualification')
            mentor_profile.full_address = request.POST.get('full_address')
            mentor_profile.city = request.POST.get('city')
            mentor_profile.district = request.POST.get('district')
            mentor_profile.state = request.POST.get('state')
            mentor_profile.pincode = request.POST.get('pincode')
            mentor_profile.store_or_advisor = request.POST.get('store_or_advisor')
            mentor_profile.job_title = request.POST.get('job_title')
            mentor_profile.total_experience_years = request.POST.get('total_experience_years')
            mentor_profile.current_employer = request.POST.get('current_employer')
            mentor_profile.location = request.POST.get('location')
            mentor_profile.work_history = request.POST.get('work_history')
            mentor_profile.course_level = request.POST.get('course_level')
            mentor_profile.course_name = request.POST.get('course_name')
            
            # Handle file uploads
            if 'passport_photo' in request.FILES:
                mentor_profile.passport_photo = request.FILES['passport_photo']
            if 'id_proof' in request.FILES:
                mentor_profile.id_proof = request.FILES['id_proof']
            
            mentor_profile.save()
            
            # Return success response for Toastify
            return JsonResponse({
                'status': 'success',
                'message': 'Profile updated successfully!'
            })
            
        except Exception as e:
            # Return error response for Toastify
            return JsonResponse({
                'status': 'error',
                'message': f'Error updating profile: {str(e)}'
            }, status=400)
    
    # For GET requests, render the form with current data
    context = {
        'user': user,
        'mentor_profile': mentor_profile
    }
    return render(request, 'edit_profile.html', context)


@login_required
def mentor_change_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new-password")
        confirm_password = request.POST.get("confirm-password")

        if new_password != confirm_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Passwords do not match!'
                }, status=400)
            return redirect("/mentor/mentor_change_password/")

        if len(new_password) < 8:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Password must be at least 8 characters long.'
                }, status=400)
            return redirect("/mentor/mentor_change_password/")

        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Password updated successfully!',
                'redirect_url': '/mentor/mentor_change_password/'
            })
        return redirect("/mentor/mentor_change_password")

    return render(request, "mentor_change_password.html")