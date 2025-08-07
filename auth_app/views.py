from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login
from datetime import datetime
from django.http import JsonResponse

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')  
        confirm_password = request.POST.get('confirm_password')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email already registered.'})

        # Check if phone number already exists
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            return render(request, 'registration.html', {'error': 'Phone already registered.'})

        # Check password match
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

        # Create user (inactive until OTP verified)
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            phone_number=phone_number,
            is_active=False  # 🚨 inactive until OTP verified
        )

        # Generate OTP
        otp_code = generate_otp()
        UserOTP.objects.create(user=user, otp_code=otp_code)

        # TODO: Send OTP via SMS/Email
        print(f"OTP for {email}: {otp_code}")  # 👀 Debug (replace with email/sms service)

        # Redirect to OTP verification page
        return redirect('verify_otp', user_id=user.id)

    return render(request, 'registration.html')

def verify_otp(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        print(otp_code)

        # ✅ Master OTP bypass
        if otp_code == "123456":
            user.is_active = True
            user.save()
            UserOTP.objects.filter(user=user).delete()  # clean up OTPs
            login(request, user)   # 🔑 login user directly
            return redirect('select_category')  # redirect wherever you want after login

        try:
            user_otp = UserOTP.objects.get(user=user, otp_code=otp_code)
            if not user_otp.is_expired():
                user.is_active = True
                user.save()
                user_otp.delete()
                login(request, user)   # 🔑 login user directly
                return redirect('select_category')
            else:
                return render(request, 'verify_otp.html', {
                    'error': 'OTP expired',
                    'user_id': user_id
                })
        except UserOTP.DoesNotExist:
            return render(request, 'verify_otp.html', {
                'error': 'Invalid OTP',
                'user_id': user_id
            })

    return render(request, 'verify_otp.html', {'user_id': user_id})

@login_required
def select_category(request):
    if request.method == "POST":
        role = request.POST.get("role")
        if role:
            request.user.role = role
            request.user.save()
            # redirect based on role or to home/dashboard
            return redirect("/participant_basic_details")
    return render(request, "selectcategory.html")


@login_required
def participant_basic_details(request):
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

        profile.save()

        print("Participant registration submitted successfully ✅")
        return redirect("dashboard")

    return render(request, "participant_basic_details.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'redirect_url': '/participants/dashboard/' if hasattr(user, 'participant_profile') else '/dashboard/'
                })
            return redirect('/participants/dashboard/' if hasattr(user, 'participant_profile') else '/dashboard/')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid email or password'
                }, status=400)
            return render(request, "login.html", {'error': 'Invalid email or password'})

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('/')