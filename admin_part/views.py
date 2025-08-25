from django.shortcuts import render,get_object_or_404,redirect
from auth_app.models import CustomUser,MentorProfile
from . models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from django.db.models import Max
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from datetime import timedelta
from decimal import Decimal
from django.utils.timezone import now
import pytz
from sajre_backend.utils import login_required_nocache 
# Create your views here.


def a_index(request):
    return render(request,'a_index.html')

def admin_check(user):
    return user.is_authenticated and user.role == 'admin'
@login_required_nocache
def admin_dashboard(request):
    # Stats
    total_participants = CustomUser.objects.filter(role="participant").count()
    total_mentors = CustomUser.objects.filter(role="mentor").count()
    total_vendors = CustomUser.objects.filter(role="vendor").count()
    total_courses = Course.objects.count()
    total_categories = CompetitionCategory.objects.count()

    # Revenue
    total_revenue = (
        ParticipantPayment.objects.filter(status="paid")
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    monthly_revenue = (
        ParticipantPayment.objects.filter(status="paid", created_at__month=now().month)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    # Recent 5 payments
    recent_payments = (
        ParticipantPayment.objects.filter(status="paid")
        .select_related("participant__user")
        .order_by("-created_at")[:5]
    )

    # ✅ Revenue trend grouped by month (cross-database compatible)
    revenue_trend = (
        ParticipantPayment.objects.filter(status="paid")
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    # Convert months to labels for the chart (like Jan, Feb, …)
    revenue_trend = [
        {
            "month": r["month"].strftime("%b %Y") if r["month"] else "Unknown",
            "total": r["total"],
        }
        for r in revenue_trend
    ]

    context = {
        "total_participants": total_participants,
        "total_mentors": total_mentors,
        "total_vendors": total_vendors,
        "total_courses": total_courses,
        "total_categories": total_categories,
        "total_revenue": total_revenue,
        "monthly_revenue": monthly_revenue,
        "recent_payments": recent_payments,
        "revenue_trend": revenue_trend,
    }
    return render(request, "admin_dashboard.html", context)
    


@login_required_nocache
def vendor_list(request):
    # Filter users with vendor role
    vendors = CustomUser.objects.filter(role='vendor')
    
    context = {
        'vendors': vendors
    }
    return render(request, 'vendor_list.html', context)


@login_required_nocache
def vendor_details(request, vendor_id):
    vendor = get_object_or_404(CustomUser, id=vendor_id, role="vendor")

    # ✅ Count referred users
    referred_users = CustomUser.objects.filter(referred_by=vendor)

    total_vendors = referred_users.filter(role="vendor").count()
    total_mentors = referred_users.filter(role="mentor").count()
    total_participants = referred_users.filter(role="participant").count()
    print(total_participants)
    # ✅ Enrolled participants
    enrolled_participants = Participant.objects.filter(user__referred_by=vendor).count()

    # ✅ Fetch profile even if vendor has one in MentorProfile
    mentor_profile = MentorProfile.objects.filter(user=vendor).first()

    context = {
        "vendor": vendor,
        "mentor_profile": mentor_profile,   # <-- fixed
        "total_vendors": total_vendors,
        "total_mentors": total_mentors,
        "total_participants": total_participants,
        "enrolled_participants": enrolled_participants,
    }
    return render(request, "vendor_details.html", context)


@login_required_nocache
def mentors(request):
    # Filter users with vendor role
    mentors = CustomUser.objects.filter(role='mentor')
    
    context = {
        'mentors': mentors
    }
    return render(request, 'mentors.html', context)

@login_required_nocache
def view_mentor_details(request, mentor_id):
    mentor = get_object_or_404(CustomUser, id=mentor_id, role="mentor")

    # ✅ Count referred users
    referred_users = CustomUser.objects.filter(referred_by=mentor)

    total_mentors = referred_users.filter(role="mentor").count()
    total_participants = referred_users.filter(role="participant").count()
    print(total_participants)
    # ✅ Enrolled participants
    enrolled_participants = Participant.objects.filter(user__referred_by=mentor).count()

    # ✅ Fetch profile even if vendor has one in MentorProfile
    mentor_profile = MentorProfile.objects.filter(user=mentor).first()

    context = {
        "mentor": mentor,
        "mentor_profile": mentor_profile,   # <-- fixed
        "total_mentors": total_mentors,
        "total_participants": total_participants,
        "enrolled_participants": enrolled_participants,
    }
    return render(request, "view_mentor_details.html", context)

@login_required_nocache
def participants_list(request):
    participants = CustomUser.objects.filter(role='participant')
    
    context = {
        'participants': participants 
    }
    return render(request, 'participants_list.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CompetitionCategory, Level, Round

# Competition Category CRUD Views
@login_required_nocache
def competition_category_list(request):
    categories = CompetitionCategory.objects.all()
    return render(request, 'competition_category_list.html', {'categories': categories})

@login_required_nocache
def add_competition_category(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        age_min = request.POST.get("age_min")
        age_max = request.POST.get("age_max")
        theme = request.POST.get("theme", "").strip() or None
        fee = request.POST.get("fee")
        level_start = request.POST.get("level_start")
        prize_1 = request.POST.get("prize_1")
        prize_2 = request.POST.get("prize_2")
        prize_3 = request.POST.get("prize_3")

        # ✅ Validations
        errors = []

        if not name:
            errors.append("Name is required.")
        if not age_min or not age_min.isdigit() or int(age_min) < 0:
            errors.append("Age Min must be a valid positive number.")
        if age_max and (not age_max.isdigit() or int(age_max) < int(age_min)):
            errors.append("Age Max must be greater than Age Min.")
        if not fee or float(fee) < 0:
            errors.append("Fee must be a positive amount.")
        if not level_start or int(level_start) < 1:
            errors.append("Level Start must be at least 1.")
        if not prize_1 or float(prize_1) <= 0:
            errors.append("Prize 1 must be greater than 0.")
        if not prize_2 or float(prize_2) <= 0:
            errors.append("Prize 2 must be greater than 0.")
        if not prize_3 or float(prize_3) <= 0:
            errors.append("Prize 3 must be greater than 0.")

        # ✅ Return errors via JSON
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # ✅ Save category
        CompetitionCategory.objects.create(
            name=name,
            age_min=int(age_min),
            age_max=int(age_max) if age_max else None,
            theme=theme,
            fee=float(fee),
            level_start=int(level_start),
            prize_1=float(prize_1),
            prize_2=float(prize_2),
            prize_3=float(prize_3)
        )

        return JsonResponse({"status": "success", "message": "Category added successfully!"})

    return render(request, "add_competition_category.html")


@require_POST
def delete_competition_category(request, pk):
    try:
        category = CompetitionCategory.objects.get(pk=pk)
        category.delete()
        return JsonResponse({"status": "success", "message": "Category deleted successfully!"})
    except CompetitionCategory.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Category not found."}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required_nocache
def edit_competition_category(request, pk):
    category = get_object_or_404(CompetitionCategory, pk=pk)

    if request.method == "GET":
        # render form with prefilled data
        return render(request, "edit_competition_category.html", {"category": category})

    elif request.method == "POST":
        try:
            category.name = request.POST.get("name")
            category.age_min = request.POST.get("age_min")
            category.age_max = request.POST.get("age_max") or None
            category.theme = request.POST.get("theme")
            category.fee = request.POST.get("fee")
            category.level_start = request.POST.get("level_start")
            category.prize_1 = request.POST.get("prize_1")
            category.prize_2 = request.POST.get("prize_2")
            category.prize_3 = request.POST.get("prize_3")
            category.save()

            return JsonResponse({"status": "success", "message": "Category updated successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
        
@login_required_nocache
def get_category_levels(request, category_id):
    category = get_object_or_404(CompetitionCategory, id=category_id)
    levels = category.levels.all().order_by("number")
    
    levels_data = [
        {
            "id": level.id,
            "number": level.number,
            "description": level.description or "No description",
            "registration_start_date" : level.registration_start_date,
            "registration_end_date" : level.registration_end_date
        }
        for level in levels
    ]
    return JsonResponse({
        "category": category.name, 
        "category_id": category.id,  # Make sure this is included
        "levels": levels_data
    })

@require_POST
def add_level(request, category_id):
    number = request.POST.get("number")
    description = request.POST.get("description")
    start_date = request.POST.get("registration_start_date")
    end_date = request.POST.get("registration_end_date")

    category = get_object_or_404(CompetitionCategory, id=category_id)

    # Check if level with this number already exists in the same category
    if Level.objects.filter(category=category, number=number).exists():
        return JsonResponse({
            "status": "error",
            "message": "Level with this number already exists"
        })

    level = Level.objects.create(
        category=category,
        number=number,
        description=description,
        registration_start_date=start_date,
        registration_end_date=end_date
    )

    return JsonResponse({
        "status": "success",
        "level": {
            "id": level.id,
            "number": level.number,
            "description": level.description,
            "registration_start_date": str(level.registration_start_date),
            "registration_end_date": str(level.registration_end_date),
        }
    })

@require_POST
def delete_level(request, level_id):
    try:
        level = Level.objects.get(id=level_id)
        level.delete()
        return JsonResponse({"status": "success"})
    except Level.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Level not found"}, status=404)

@login_required_nocache
def level_info(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    rounds = level.rounds.all().prefetch_related("schedules")

    return render(request, "level_info.html", {
        "level": level,
        "rounds": rounds
    })

@login_required_nocache
def add_round(request):
    if request.method == "POST":
        try:
            level_id = request.POST.get("level_id")
            number = request.POST.get("number")
            mode = request.POST.get("mode")
            description = request.POST.get("description")
            last_registration_date = request.POST.get("last_registration_date")

            level = Level.objects.get(id=level_id)

            round_obj = Round.objects.create(
                level=level,
                number=number,
                mode=mode,
                description=description,
                last_registration_date=parse_date(last_registration_date) if last_registration_date else None
            )

            return JsonResponse({"success": True, "round_id": round_obj.id})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


@require_POST
def add_or_update_schedule(request):
    try:
        round_id = request.POST.get("round_id")
        schedule_id = request.POST.get("schedule_id")

        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        total_seats = request.POST.get("total_seats")

        if not round_id:
            return JsonResponse({"success": False, "error": "Round ID is required"})

        round_obj = get_object_or_404(Round, id=round_id)

        # If schedule_id exists → update
        if schedule_id:
            schedule = get_object_or_404(RoundSchedule, id=schedule_id, round=round_obj)
            schedule.date = date
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.total_seats = total_seats
            schedule.save()
            return JsonResponse({"success": True, "message": "Schedule updated successfully!"})

        # Else create new schedule
        else:
            schedule = RoundSchedule.objects.create(
                round=round_obj,
                date=date,
                start_time=start_time,
                end_time=end_time,
                total_seats=total_seats,
            )
            return JsonResponse({"success": True, "message": "Schedule created successfully!"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# @csrf_exempt
# def update_last_date(request):
#     if request.method == "POST":
#         round_id = request.POST.get("round_id")
#         start_date_str = request.POST.get("registration_start_date")
#         registration_end_date = request.POST.get("registration_end_date")

#         try:
#             round_obj = Round.objects.get(id=round_id)
#             last_date = parse_date(date_str)

#             if not last_date:
#                 return JsonResponse({"success": False, "error": "Invalid date format"})

#             # Prevent past dates
#             from datetime import date as dt_date
#             if last_date < dt_date.today():
#                 return JsonResponse({"success": False, "error": "Cannot set past date."})

#             round_obj.last_registration_date = last_date
#             round_obj.save()

#             return JsonResponse({"success": True, "message": "Last registration date updated successfully!"})

#         except Round.DoesNotExist:
#             return JsonResponse({"success": False, "error": "Round not found."})

#     return JsonResponse({"success": False, "error": "Invalid request"})

@csrf_exempt
def edit_level(request, level_id):
    if request.method == "POST":
        try:
            level = Level.objects.get(id=level_id)
            number = request.POST.get("number")
            description = request.POST.get("description")
            start_date = parse_date(request.POST.get("registration_start_date"))
            end_date = parse_date(request.POST.get("registration_end_date"))

            # Prevent duplicate numbers within same category
            if Level.objects.filter(category=level.category, number=number).exclude(id=level_id).exists():
                return JsonResponse({"status": "error", "message": "Level with this number already exists"})

            level.number = number
            level.description = description
            level.registration_start_date = start_date
            level.registration_end_date = end_date
            level.save()

            return JsonResponse({
                "status": "success",
                "level": {
                    "id": level.id,
                    "number": level.number,
                    "description": level.description,
                    "registration_start_date": str(level.registration_start_date) if level.registration_start_date else None,
                    "registration_end_date": str(level.registration_end_date) if level.registration_end_date else None,
                }
            })
        except Level.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Level not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})

@login_required_nocache
def view_faq(request):
    faq_counts = FAQ.objects.values("role_type").annotate(count=Count("id"))
    faq_data = {item["role_type"]: item["count"] for item in faq_counts}

    roles = [
        ("vendor", "Vendor"),
        ("mentor", "Mentor"),
        ("participant", "Participant"),
        ("jury", "Jury"),   # lowercase for consistency
        ("general", "General"),
    ]

    # Build role list with counts
    roles_with_counts = [(role, label, faq_data.get(role, 0)) for role, label in roles]

    context = {
        "roles_with_counts": roles_with_counts,
        "faq_role_choices": FAQ.ROLE_CHOICES,
    }
    return render(request, "view_faq.html", context)


@login_required_nocache
def add_faq(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        role_type = request.POST.get("role_type")

        if not question or not answer or not role_type:
            return JsonResponse({"error": "All fields are required"}, status=400)

        faq = FAQ.objects.create(
            question=question,
            answer=answer,
            role_type=role_type
        )

        # ✅ Get updated count for this role
        new_count = FAQ.objects.filter(role_type=role_type).count()

        return JsonResponse({
            "message": "FAQ added successfully",
            "role_type": role_type,
            "new_count": new_count
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required_nocache
def view_faqs_by_role(request, role):
    role_label = dict(FAQ.ROLE_CHOICES).get(role, "FAQs")  # Get display name
    faqs = FAQ.objects.filter(role_type=role).order_by("-created_at")

    context = {
        "role": role,
        "role_label": role_label,
        "faqs": faqs,
    }
    return render(request, "view_faqs_by_role.html", context)


@require_POST
def delete_faq(request, faq_id):
    try:
        faq = FAQ.objects.get(id=faq_id)
        faq.delete()
        return JsonResponse({"success": True, "message": "FAQ deleted successfully"})
    except FAQ.DoesNotExist:
        return JsonResponse({"success": False, "message": "FAQ not found"}, status=404)


@login_required_nocache
def enrolled_list(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    participants = Participant.objects.filter(level=level).select_related("user", "category")

    # Convert to IST
    ist = pytz.timezone("Asia/Kolkata")

    for p in participants:
        latest_payment = ParticipantPayment.objects.filter(
            participant=p, status="paid"
        ).order_by("-payment_date").first()

        p.latest_payment_date = (
            timezone.localtime(latest_payment.payment_date, ist)
            if latest_payment and latest_payment.payment_date else None
        )

    context = {
        "level": level,
        "participants": participants,
    }
    return render(request, "enrolled_list.html", context)

@login_required_nocache
def participant_detail(request, participant_id):
    user = get_object_or_404(CustomUser, id=participant_id, role="participant")
    profile = getattr(user, "participant_profile", None)

    context = {
        "user": user,
        "profile": profile,
    }
    return render(request, "participant_detail.html", context)

@login_required_nocache
def tutor_enquiries(request):
    enquiries = TutorInquiry.objects.all().order_by("-submitted_at")
    return render(request, "tutor_enquiries.html", {"enquiries": enquiries})

@login_required_nocache
def add_course(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        name = request.POST.get("name")
        subtitle = request.POST.get("subtitle")
        image = request.FILES.get("image")

        errors = []
        if not name:
            errors.append("Course name is required.")
        if not subtitle:
            errors.append("Course subtitle is required.")

        if errors:
            return JsonResponse({"status": "error", "errors": errors})

        Course.objects.create(
            name=name,
            subtitle=subtitle,
            image=image
        )
        return JsonResponse({"status": "success", "message": "Course added successfully!"})

    return render(request, "add_course.html")

@login_required_nocache
def view_courses(request):
    courses = Course.objects.all().order_by('-id')  # latest first
    return render(request, 'view_course.html', {'courses': courses})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        name = request.POST.get("name")
        subtitle = request.POST.get("subtitle")
        image = request.FILES.get("image")

        if not name:
            return JsonResponse({"success": False, "error": "Course name is required."})

        # Update course fields
        course.name = name
        course.subtitle = subtitle
        if image:
            course.image = image
        course.save()

        return JsonResponse({"success": True, "message": "Course updated successfully!"})

    return render(request, "edit_course.html", {"course": course})


@csrf_exempt
def delete_course(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        course.delete()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":  
            return JsonResponse({"success": True, "message": "Course deleted successfully!"})

        return redirect("/admin_part/courses/")

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@login_required_nocache
@require_POST
def delete_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    return JsonResponse({"success": True, "message": "FAQ deleted successfully!"})