from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from auth_app.models import CustomUser
from admin_part.models import Participant,CompetitionCategory
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from auth_app.models import MentorProfile
import json
from sajre_backend.utils import login_required_nocache 

from django.views.decorators.http import require_POST

# Create your views here.
@login_required_nocache
def mentor_dashboard(request):
    # Count students referred by this user
    referred_students_count = CustomUser.objects.filter(
        referred_by=request.user,
        role="participant"
    ).count()
    print("Total referred students:", referred_students_count)

    # Count enrolled students
    enrolled_students_count = Participant.objects.filter(
        user__referred_by=request.user,
        has_paid=True
    ).count()
    print("Enrolled referred students:", enrolled_students_count)

    # Get all categories
    categories = CompetitionCategory.objects.all()
    
    # Get category-wise data for pie charts
    category_data = []
    for category in categories:
        total = 0
        enrolled = 0
    
        # loop through all referred users and use the same matching logic
        for user in CustomUser.objects.filter(referred_by=request.user, role="participant"):
            # check matching category
            matched = None
            if hasattr(user, "participant_profile") and user.participant_profile.age:
                age = user.participant_profile.age
                if age >= category.age_min and (category.age_max is None or age <= category.age_max):
                    matched = True
    
            if matched:
                total += 1
                # if matched and paid → enrolled++
                if hasattr(user, "participant") and user.participant.has_paid:
                    enrolled += 1
    
        category_data.append({
            "name": category.name,
            "total": total,
            "enrolled": enrolled,
            "not_enrolled": total - enrolled
        })
        # Fetch participants with their matching category
    participants = []
    for user in CustomUser.objects.filter(
        referred_by=request.user,
        role="participant"
    ).select_related("participant", "participant__category", "participant_profile"):
        
        # Find matching category based on age
        matching_category = None
        if hasattr(user, 'participant_profile') and user.participant_profile.age:
            age = user.participant_profile.age
            for category in categories:
                if (age >= category.age_min and 
                        (category.age_max is None or age <= category.age_max)):
                    matching_category = category
                    break

        print(f"User: {user.full_name} → Matching Category: {matching_category}")

        participants.append({
            'user': user,
            'matching_category': matching_category
        })

    return render(request, 'mentor_dashboard.html', {
        'referred_students_count': referred_students_count,
        'enrolled_students_count': enrolled_students_count,
        'category_data': category_data,
        'participants': participants,
        'categories': categories,
    })


@login_required_nocache
def create_mentor_profile(request):
    """
    First time profile creation view for vendor.
    """
    user = request.user

    if request.method == "POST":
        try:
            # Handle empty values for decimal field
            total_experience_years = request.POST.get("total_experience_years")
            if total_experience_years == '':
                total_experience_years = None
                
            MentorProfile.objects.create(
                user=user,
                higher_qualification=request.POST.get("higher_qualification"),
                full_address=request.POST.get("full_address"),
                city=request.POST.get("city"),
                district=request.POST.get("district"),
                state=request.POST.get("state"),
                pincode=request.POST.get("pincode"),
                store_or_advisor=request.POST.get("store_or_advisor"),
                job_title=request.POST.get("job_title"),
                total_experience_years=total_experience_years,  # Use the processed value
                current_employer=request.POST.get("current_employer"),
                location=request.POST.get("location"),
                work_history=request.POST.get("work_history"),
                course_level=request.POST.get("course_level"),
                course_name=request.POST.get("course_name"),
                passport_photo=request.FILES.get("passport_photo"),
                id_proof=request.FILES.get("id_proof")
            )
            return JsonResponse({"status": "success", "message": "Profile created successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error creating profile: {str(e)}"}, status=400)

    return render(request, "create_mentor_profile.html", {"user": user, "vendor_profile": None})

@login_required_nocache
def edit_profile(request):
    user = request.user
    try:
        mentor_profile = user.mentor_profile
    except MentorProfile.DoesNotExist:
        # Redirect to the page where user can create the profile
        return redirect('create_mentor_profile')
    
    if request.method == 'POST':
        try:
            # Handle empty values for decimal field
            total_experience_years = request.POST.get("total_experience_years")
            if total_experience_years == '':
                total_experience_years = None
            
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
            mentor_profile.total_experience_years = total_experience_years  # Use processed value
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
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    return render(request, 'edit_profile.html', context)


@login_required_nocache
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

@login_required_nocache
def m_terms(request):
    return render(request, 'm_terms.html')

@require_POST
@login_required_nocache
def update_terms_status(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.accepted_terms = True
            user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required_nocache
def m_working_on(request):
    return render(request,'m_working_on.html')


from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
@login_required_nocache
def get_participant_details(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id, referred_by=request.user)
        profile = user.participant_profile
        
        data = {
            'full_name': user.full_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'photo': profile.photo.url if profile.photo else None,
            'age': profile.age,
            'dob': profile.dob.strftime('%d %b, %Y') if profile.dob else None,
            'father_name': profile.father_name,
            'mother_name': profile.mother_name,
            'full_address': profile.full_address,
            'city': profile.city,
            'state': profile.state,
            'pincode': profile.pincode,
            'school_name': profile.school_name,
            'university_name': profile.university_name,
            'grade': profile.grade,
            'stream': profile.stream,
            'school_board': profile.school_board,
            'university': profile.university,
            'category': user.participant.category.name if hasattr(user, 'participant') and user.participant.category else None,
            'has_paid': user.participant.has_paid if hasattr(user, 'participant') else False,
            'registration_date': user.date_joined.strftime('%d %b, %Y'),
            'referral_code': user.referral_code,
        }
        
        return JsonResponse(data)
    
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Participant not found'}, status=404)