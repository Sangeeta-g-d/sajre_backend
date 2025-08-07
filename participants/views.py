from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from auth_app.models import ParticipantProfile
from datetime import datetime
from admin_part.models import RoundSchedule,CompetitionCategory,Participant,ParticipantPayment,Level,Round
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import F
from decimal import Decimal
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.utils.timezone import now
import razorpay
from django.conf import settings
# Create your views here.

@login_required
def dashboard(request):
    try:
        profile = ParticipantProfile.objects.get(user=request.user)
    except ParticipantProfile.DoesNotExist:
        return render(request, 'dashboard.html')

    upcoming_round = None
    is_enrolled = False

    if profile.age:
        category = CompetitionCategory.objects.filter(
            age_min__lte=profile.age
        ).filter(
            Q(age_max__gte=profile.age) | Q(age_max__isnull=True)
        ).first()

        if category:
            today = now().date()
            # get earliest upcoming schedule
            upcoming_round = RoundSchedule.objects.filter(
                round__level__category=category,
                date__gte=today
            ).order_by("date", "start_time").first()

            # ✅ check if participant exists and has paid
            try:
                participant = Participant.objects.get(user=request.user, category=category)
                if participant.has_paid:
                    is_enrolled = True
            except Participant.DoesNotExist:
                pass

    return render(request, 'dashboard.html', {
        "upcoming_round": upcoming_round,
        "is_enrolled": is_enrolled
    })


@login_required
def terms(request):
    profile = ParticipantProfile.objects.get(user=request.user)
    
    category = CompetitionCategory.objects.filter(
        age_min__lte=profile.age
    ).filter(
        Q(age_max__gte=profile.age) | Q(age_max__isnull=True)
    ).first()

    base_fee = category.fee if category else 0
    transaction_fee = round(float(base_fee) * 0.03, 2)
    platform_fee = round(float(base_fee) * 0.10, 2)
    gst = round((float(base_fee) + transaction_fee + platform_fee) * 0.18, 2)
    total = round(float(base_fee) + transaction_fee + platform_fee + gst, 2)

    level = None
    current_round = None
    if category:
        # default level = category.level_start
        level = Level.objects.filter(category=category, number=category.level_start).first()
        
        # pick first round in that level
        current_round = Round.objects.filter(level=level).order_by("number").first()
    request.session["participant_data"] = {
        "age": profile.age,
        "category_id": category.id if category else None,
        "level_id": level.id if level else None,
        "round_id": current_round.id if current_round else None,
    }
    return render(request, "terms.html", {
        "category": category,
        "base_fee": base_fee,
        "transaction_fee": transaction_fee,
        "platform_fee": platform_fee,
        "gst": gst,
        "total": total,
        "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID,   # ✅ important
    })

@csrf_exempt
def payment_success(request):
    if request.method == 'GET':
        payment_id = request.GET.get('payment_id')

        if not payment_id:
            return redirect(reverse('payment-failed') + '?error=no_payment_id')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            payment = client.payment.fetch(payment_id)

            participant, created = Participant.objects.get_or_create(
                user=request.user,
                defaults={
                    "age": request.session.get("participant_data", {}).get("age"),
                    "category_id": request.session.get("participant_data", {}).get("category_id"),
                    "level_id": request.session.get("participant_data", {}).get("level_id"),
                    "current_round_id": request.session.get("participant_data", {}).get("round_id"),
                }
            )

            try:
                payment_record = ParticipantPayment.objects.create(
                    participant=participant,
                    razorpay_payment_id=payment_id,
                    razorpay_order_id=payment.get('order_id'),
                    amount=Decimal(payment['amount']) / Decimal(100),
                    currency=payment['currency'],
                    status='paid'
                )
                payment_record.mark_as_paid(payment_id)

                # ✅ Decrement RoundSchedule seats after payment success
                round_id = request.session.get("participant_data", {}).get("round_id")
                if round_id:
                    schedule = RoundSchedule.objects.filter(
                        round_id=round_id,
                        booked_seats__lt=F("total_seats")  # ensure seats available
                    ).first()
                    if schedule:
                        schedule.booked_seats += 1
                        schedule.save()

                return render(request, 'payment_success.html', {
                    'payment_id': payment_id,
                    'title': 'Payment Successful',
                    'amount': payment['amount'] / 100
                })

            except Exception as e:
                return redirect(reverse('payment-failed') + f'?error=db_error&message={str(e)}')

        except Exception as e:
            return redirect(reverse('payment-failed') + f'?error=unexpected_error&message={str(e)}')


def payment_failed(request):
    error_code = request.GET.get('error', 'unknown_error')
    error_message = request.GET.get('message', 'An unknown error occurred')
    
    print(f"Payment failed - Error: {error_code}, Message: {error_message}")
    
    return render(request, 'payment_failed.html', {
        'error_code': error_code,
        'error_message': error_message,
        'title': 'Payment Failed'
    })



@csrf_exempt
def update_terms_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            accepted = data.get("accepted_terms", False)

            request.user.accepted_terms = bool(accepted)
            request.user.save()

            return JsonResponse({"status": "success", "accepted_terms": request.user.accepted_terms})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
def create_razorpay_order(request):
    if request.method == "POST":
        amount = request.POST.get("amount")   # comes from frontend (₹ in paisa)
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            order = client.order.create({
                "amount": int(amount),    # amount in paisa
                "currency": "INR",
                "payment_capture": 1
            })

            return JsonResponse({"status": "success", "order": order})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@login_required
def profile(request):
    try:
        profile = ParticipantProfile.objects.get(user=request.user)
    except ParticipantProfile.DoesNotExist:
        return redirect('dashboard')

    if request.method == 'POST':
        try:
            # Update user fields
            request.user.full_name = request.POST.get('full_name', request.user.full_name)
            request.user.save()
            
            profile.grade = request.POST.get('grade', profile.grade)

            # ✅ Convert dob string to date
            dob_str = request.POST.get('dob')
            if dob_str:
                try:
                    profile.dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                except ValueError:
                    pass  # keep old value if parsing fails

            profile.full_address = request.POST.get('address', profile.full_address)
            profile.school_name = request.POST.get('school_name', profile.school_name)

            # Save uploaded file if provided
            if 'edu_doc' in request.FILES:
                profile.edu_doc = request.FILES['edu_doc']

            profile.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('profile')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})

    # Handle GET request
    context = {'profile': profile}
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(context)
    return render(request, 'profile.html', context)

@login_required
def update_profile_photo(request):
    if request.method == "POST":
        try:
            profile = ParticipantProfile.objects.get(user=request.user)
        except ParticipantProfile.DoesNotExist:
            
            return redirect("profile")

        if "photo" in request.FILES:
            profile.photo = request.FILES["photo"]
            profile.save()

    return redirect("profile")


@login_required
def change_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new-password")
        confirm_password = request.POST.get("confirm-password")

        if new_password != confirm_password:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Passwords do not match!'
                }, status=400)
            return redirect("change_password")

        if len(new_password) < 8:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Password must be at least 8 characters long.'
                }, status=400)
            return redirect("change_password")

        user = request.user
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Password updated successfully!',
                'redirect_url': '/participants/dashboard/'
            })
        return redirect("dashboard")

    return render(request, "change_password.html")