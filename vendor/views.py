from django.shortcuts import render,redirect
from auth_app.models import CustomUser
from admin_part.models import Participant,CompetitionCategory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash

# Create your views here.


def vendor_dashboard(request):
    referred_mentors_count = CustomUser.objects.filter(
        referred_by=request.user,
        role="mentor"
    ).count()

    # Default value to avoid UnboundLocalError
    referred_students_count = CustomUser.objects.filter(
        referred_by=request.user,
        role="participant"
    ).count()

    # If 5+ mentors referred, mark this user as active vendor
    if referred_mentors_count >= 5 and request.user.role == "mentor":
        request.user.active_vendor = True
        request.user.save(update_fields=["active_vendor"])

    enrolled_students_count = Participant.objects.filter(
        user__referred_by=request.user,
        has_paid=True
    ).count()

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
            'not_enrolled': max(total - enrolled, 0)
        })

    participants_list = CustomUser.objects.filter(
        referred_by=request.user,
        role="participant"
    ).select_related("participant", "participant__category")

    context = {
        'referred_mentors_count': referred_mentors_count,
        'referred_students_count': referred_students_count,
        'enrolled_students_count': enrolled_students_count,
        'category_data': category_data,
        'participants_list': participants_list,
    }
    return render(request, 'vendor_dashboard.html', context)


@login_required
def edit_vendor_profile(request):
    user = request.user
    vendor_profile = user.mentor_profile
    
    if request.method == 'POST':
        try:
            # Update User fields
            user.full_name = request.POST.get('full_name', user.full_name)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            user.save()
            
            # Update MentorProfile fields
            vendor_profile.higher_qualification = request.POST.get('higher_qualification')
            vendor_profile.full_address = request.POST.get('full_address')
            vendor_profile.city = request.POST.get('city')
            vendor_profile.district = request.POST.get('district')
            vendor_profile.state = request.POST.get('state')
            vendor_profile.pincode = request.POST.get('pincode')
            vendor_profile.store_or_advisor = request.POST.get('store_or_advisor')
            vendor_profile.job_title = request.POST.get('job_title')
            vendor_profile.total_experience_years = request.POST.get('total_experience_years')
            vendor_profile.current_employer = request.POST.get('current_employer')
            vendor_profile.location = request.POST.get('location')
            vendor_profile.work_history = request.POST.get('work_history')
            vendor_profile.course_level = request.POST.get('course_level')
            vendor_profile.course_name = request.POST.get('course_name')
            
            # Handle file uploads
            if 'passport_photo' in request.FILES:
                vendor_profile.passport_photo = request.FILES['passport_photo']
            if 'id_proof' in request.FILES:
                vendor_profile.id_proof = request.FILES['id_proof']
            
            vendor_profile.save()
            
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
        'vendor_profile': vendor_profile
    }
    return render(request, 'edit_vendor_profile.html', context)


@login_required
def vendor_change_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new-password")
        confirm_password = request.POST.get("confirm-password")

        if new_password != confirm_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Passwords do not match!'
                }, status=400)
            return redirect("/vendor/vendor_change_password/")

        if len(new_password) < 8:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Password must be at least 8 characters long.'
                }, status=400)
            return redirect("/vendor/vendor_change_password/")

        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Password updated successfully!',
                'redirect_url': '/vendor/vendor_change_password/'
            })
        return redirect("/vendor/vendor_change_password")

    return render(request, "vendor_change_password.html")