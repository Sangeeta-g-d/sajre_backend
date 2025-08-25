from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login
from datetime import datetime
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .utils.exotel import send_otp_sms
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

@never_cache
@csrf_protect
def register(request):
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        # Determine redirect URL based on user role
        if not request.user.role or request.user.role == "customer":
            return redirect("/auth/select_category/")
        elif request.user.role == "mentor":
            return redirect("/mentor/mentor_dashboard/")
        elif request.user.role == "vendor":
            return redirect("/vendor/vendor_dashboard/")
        elif request.user.role == "participant":
            return redirect("/participants/dashboard/")
        elif request.user.is_superuser:
            return redirect("/admin_part/admin_dashboard/")
        else:
            return redirect("/working_on/")
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # ✅ Validate phone number (must be 10 digits only)
        if not (phone_number.isdigit() and len(phone_number) == 10):
            response = render(request, 'registration.html', {'error': 'Phone number must be exactly 10 digits.'})
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            response = render(request, 'registration.html', {'error': 'Email already registered.'})
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        # Check if phone number already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            response = render(request, 'registration.html', {'error': 'Phone number already registered.'})
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        # Check password match
        if password != confirm_password:
            response = render(request, 'registration.html', {'error': 'Passwords do not match.'})
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        try:
            with transaction.atomic():   # ✅ Wrap in transaction
                # Create user (inactive until OTP verified)
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    phone_number=phone_number,
                    is_active=False
                )

                # Generate OTP
                otp_code = generate_otp()
                UserOTP.objects.create(user=user, otp_code=otp_code)

                # ✅ Send OTP (phone_number is already 10 digits)
                send_otp_sms(phone_number, otp_code)

            # ✅ If everything succeeds, commit & redirect
            response = redirect('verify_otp', user_id=user.id)
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        except Exception as e:
            # Rollback happens automatically if exception raised
            print("Registration failed:", e)
            response = render(request, 'registration.html', {
                'error': 'Something went wrong. Please try again.'
            })
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

    # For GET requests, also set no-cache headers
    response = render(request, 'registration.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def csrf_failure(request, reason=""):
    # Instead of showing the default 403 page,
    # just redirect back to signup page with a toast message
    return render(request, 'registration.html', {
        'error': "Session expired. Please try signing up again."
    })

def resend_otp(request, user_id):
    """
    Re-sends a new OTP and returns JSON
    """
    if request.method == "POST":
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"status": False, "message": "User not found."})

        # generate and save new otp
        otp_code = generate_otp()
        otp_obj, _ = UserOTP.objects.update_or_create(
            user=user, 
            defaults={'otp_code': otp_code, 'created_at': timezone.now()}
        )

        # send sms
        send_otp_sms(user.phone_number, otp_code)

        # calculate new remaining seconds (120 from now)
        expiry_time = otp_obj.created_at + timedelta(minutes=2)
        remaining_seconds = int((expiry_time - timezone.now()).total_seconds())

        return JsonResponse({
            "status": True,
            "message": "New OTP has been sent to your phone number.",
            "remaining_seconds": remaining_seconds
        })

    return JsonResponse({"status": False, "message": "Invalid request method."})

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

@never_cache
@csrf_protect
def verify_otp(request, user_id):
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        # Determine redirect URL based on user role
        if not request.user.role or request.user.role == "customer":
            redirect_url = "/auth/select_category/"
        elif request.user.role == "mentor":
            redirect_url = "/mentor/mentor_dashboard/"
        elif request.user.role == "vendor":
            redirect_url = "/vendor/vendor_dashboard/"
        elif request.user.role == "participant":
            redirect_url = "/participants/dashboard/"
        elif request.user.is_superuser:
            redirect_url = "/admin_part/admin_dashboard/"
        else:
            redirect_url = "/working_on/"
        
        response = redirect(redirect_url)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        response = render(request, 'verify_otp.html', {'error': 'Invalid user.'})
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    # get latest OTP for remaining_seconds countdown
    otp_obj = UserOTP.objects.filter(user=user).order_by('-created_at').first()
    remaining_seconds = 0
    if otp_obj:
        expiry_time = otp_obj.created_at + timedelta(minutes=2)
        now = timezone.now()
        remaining = (expiry_time - now).total_seconds()
        remaining_seconds = int(remaining) if remaining > 0 else 0

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')

        # ✅ Master OTP bypass
        if otp_code == "123456":
            user.is_active = True
            user.save()
            UserOTP.objects.filter(user=user).delete()
            login(request, user)
            
            response = redirect('select_category')
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        try:
            user_otp = UserOTP.objects.get(user=user, otp_code=otp_code)

            # Check if the OTP is expired
            if not user_otp.is_expired():
                user.is_active = True
                user.save()
                user_otp.delete()
                login(request, user)
                
                response = redirect('select_category')
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response
            else:
                # If expired → return to template with error string
                response = render(request, 'verify_otp.html', {
                    'error': 'OTP expired',
                    'user_id': user_id,
                    'remaining_seconds': 0
                })
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response

        except UserOTP.DoesNotExist:
            # If OTP is invalid → return with error string
            response = render(request, 'verify_otp.html', {
                'error': 'Invalid OTP',
                'user_id': user_id,
                'remaining_seconds': remaining_seconds
            })
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

    # GET request → show the page with countdown (if any)
    response = render(request, 'verify_otp.html', {
        'user_id': user_id,
        'remaining_seconds': remaining_seconds
    })
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@csrf_protect
@login_required
def select_category(request):
    # If user already has a role selected, redirect to appropriate page
    if request.user.role and request.user.role != "customer":
        # Role-based redirect
        if request.user.role == 'participant':
            # Check if participant has completed basic details
            if hasattr(request.user, 'participant_profile') and getattr(request.user.participant_profile, 'is_complete', False):
                response = redirect('/participants/dashboard/')
            else:
                response = redirect('/auth/participant_basic_details')
        elif request.user.role == 'mentor':
            # Check if mentor has completed registration
            if hasattr(request.user, 'mentor_profile') and getattr(request.user.mentor_profile, 'is_complete', False):
                response = redirect('/mentor/mentor_dashboard/')
            else:
                response = redirect('/auth/complete_profile/')
        elif request.user.role == 'vendor':
            # Check if vendor has completed registration (assuming vendor uses mentor registration)
            if hasattr(request.user, 'mentor_profile') and getattr(request.user.mentor_profile, 'is_complete', False):
                response = redirect('/vendor/vendor_dashboard/')
            else:
                response = redirect('/auth/complete_profile/')
        elif request.user.role == 'school':
            response = redirect('/working_on/')
        elif request.user.role == 'college':
            response = redirect('/working_on/')
        else:
            response = redirect('/working_on/')
        
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    if request.method == "POST":
        role = request.POST.get("role")
        if role:
            request.user.role = role

            # 👉 Generate referral code with a prefix based on role
            if role == 'mentor':
                prefix = 'M'
            elif role == 'vendor':
                prefix = 'V'
            elif role == 'participant':
                prefix = 'P'
            else:
                prefix = ''   # default / fallback

            # generate 7 random characters (to keep total length at 8)
            random_part = uuid.uuid4().hex[:7].upper()
            request.user.referral_code = prefix + random_part

            request.user.save()

            # Role-based redirect with no-cache headers
            if role == 'participant':
                response = redirect('/auth/participant_basic_details')
            elif role == 'mentor':
                response = redirect('/auth/complete_profile/')
            elif role == 'vendor':
                response = redirect('/auth/complete_profile/')
            elif role == 'school':
                response = redirect('/working_on/')
            elif role == 'college':
                response = redirect('/working_on/')
            else:
                response = redirect('/working_on/')
            
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

    # For GET requests, also set no-cache headers
    response = render(request, "selectcategory.html")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
@csrf_protect
@login_required
def participant_basic_details(request):
    # If user has already completed basic details, redirect to dashboard
    if hasattr(request.user, 'participant_profile') and request.user.participant_profile.is_complete():
        response = redirect("/participants/dashboard")
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    if request.method == "POST":
        user = request.user
        profile, created = ParticipantProfile.objects.get_or_create(user=user)

        # Step 1 fields
        profile.father_name = request.POST.get("fatherName")
        profile.mother_name = request.POST.get("motherName")
        dob_str = request.POST.get("dob")
        if dob_str:
            try:
                profile.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                profile.dob = None
        else:
            profile.dob = None
        profile.full_address = request.POST.get("fullAddress")
        profile.street_address = request.POST.get("streetAddress")
        profile.city = request.POST.get("city")
        profile.district = request.POST.get("district")
        profile.state = request.POST.get("state")
        profile.pincode = request.POST.get("pincode")
        profile.how_did_you_know = request.POST.get("howDidYouKnow")

        # ✅ Referral handling
        referral_code = request.POST.get("referralCode")
        if referral_code:
            try:
                referrer = CustomUser.objects.get(referral_code=referral_code)
                if not user.referred_by:  # only set once
                    user.referred_by = referrer
                    user.save()

                profile.referral_code_used = referral_code
                print(f"✅ Referral applied: {user.email} was referred by {referrer.email}")
            except CustomUser.DoesNotExist:
                print("❌ Invalid referral code entered")

        # Step 2 fields
        profile.school_name = request.POST.get("schoolName")
        profile.school_board = request.POST.get("schoolBoard")
        profile.school_location = request.POST.get("schoolLocation")
        profile.course_name = request.POST.get("courseName")
        profile.university = request.POST.get("university")
        profile.university_name = request.POST.get("universityName")
        profile.academic_year = request.POST.get("academicYear")
        profile.stream = request.POST.get("stream")

        # File uploads
        if request.FILES.get("dobProof"):
            profile.dob_proof = request.FILES["dobProof"]
        if request.FILES.get("photoUpload"):
            profile.photo = request.FILES["photoUpload"]

        # Mark profile as complete
        profile.is_complete = True
        profile.save()

        print("Participant registration submitted successfully ✅")
        response = redirect("dashboard")
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    # For GET requests, also set no-cache headers
    response = render(request, "participant_basic_details.html")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@never_cache
@csrf_protect
def login_view(request):
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        # Determine redirect URL based on user role
        if not request.user.role or request.user.role == "customer":
            return redirect("/auth/select_category/")
        elif request.user.role == "mentor":
            return redirect("/mentor/mentor_dashboard/")
        elif request.user.role == "vendor":
            return redirect("/vendor/vendor_dashboard/")
        elif request.user.role == "participant":
            return redirect("/participants/dashboard/")
        elif request.user.is_superuser:
            return redirect("/admin_part/admin_dashboard/")
        else:
            return redirect("/working_on/")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            
            # Set no-cache headers for the response
            response = None
            
            # Determine redirect URL
            if not user.role or user.role == "customer":
                redirect_url = "/auth/select_category/"
            elif user.role == "mentor":
                redirect_url = "/mentor/mentor_dashboard/"
            elif user.role == "vendor":
                redirect_url = "/vendor/vendor_dashboard/"
            elif user.role == "participant":
                redirect_url = "/participants/dashboard/"
            elif user.is_superuser:
                redirect_url = "/admin_part/admin_dashboard/"
            else:
                redirect_url = "/working_on/"

            # Handle AJAX login
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                response = JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'redirect_url': redirect_url
                })
            else:
                response = redirect(redirect_url)
            
            # Add headers to prevent caching
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        else:
            # Invalid credentials
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid email or password'
                }, status=400)
            return render(request, "login.html", {'error': 'Invalid email or password'})

    # For GET requests, also set no-cache headers
    response = render(request, "login.html")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response



def logout_view(request):
    logout(request)
    return redirect('/')

@never_cache
@csrf_protect
@login_required
def mentor_register(request):
    # If user has already completed mentor registration, redirect to appropriate dashboard
    if hasattr(request.user, 'mentor_profile') and request.user.mentor_profile.is_complete():
        # Redirect based on role
        if getattr(request.user, "role", "").lower() == "vendor":
            response = redirect("/vendor/vendor_dashboard/")
        else:
            response = redirect("/mentor/mentor_dashboard/")
        
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    if request.method == "POST":
        user = request.user
        profile, created = MentorProfile.objects.get_or_create(user=user)

        # Handle referral code if provided
        referral_code = request.POST.get("referralCode", "").strip()
        if referral_code:
            try:
                referred_by_user = CustomUser.objects.get(referral_code=referral_code)
                if referred_by_user != user:  # Prevent self-referral
                    user.referred_by = referred_by_user
                    user.save()
                    # Add logic here to award referral points if needed
            except CustomUser.DoesNotExist:
                pass  # Ignore invalid referral code

        # Step 1: Qualification Details
        profile.higher_qualification = request.POST.get("higherQualification")
        profile.full_address = request.POST.get("fullAddress")
        profile.store_or_advisor = request.POST.get("storeAdvisor")
        profile.city = request.POST.get("city")
        profile.district = request.POST.get("district")
        profile.state = request.POST.get("state")
        profile.pincode = request.POST.get("pincode")
        profile.course_level = request.POST.get("courseLevel")
        profile.course_name = request.POST.get("courseName")

        # Step 2: Professional Details
        profile.job_title = request.POST.get("jobTitle")
        profile.total_experience_years = request.POST.get("totalExperience") or 0
        profile.work_history = request.POST.get("workHistory")
        profile.current_employer = request.POST.get("currentEmployer")
        profile.location = request.POST.get("location")

        # File uploads
        if request.FILES.get("passportPhoto"):
            profile.passport_photo = request.FILES["passportPhoto"]
        if request.FILES.get("idProof"):
            profile.id_proof = request.FILES["idProof"]

        # Mark profile as complete
        profile.is_complete = True
        profile.save()

        print("✅ Mentor registration submitted successfully")

        # Redirect based on role with no-cache headers
        if getattr(user, "role", "").lower() == "vendor":
            response = redirect("/vendor/vendor_dashboard/")
        else:
            response = redirect("/mentor/mentor_dashboard/")
        
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    # For GET requests, also set no-cache headers
    response = render(request, "mentor_register.html")
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def forgot_password(request):
    return render(request,'forgot_password.html')


