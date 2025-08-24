from django.shortcuts import render,get_object_or_404,redirect
from auth_app.models import CustomUser,MentorProfile
from . models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date

# Create your views here.


def a_index(request):
    return render(request,'a_index.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def vendor_list(request):
    # Filter users with vendor role
    vendors = CustomUser.objects.filter(role='vendor')
    
    context = {
        'vendors': vendors
    }
    return render(request, 'vendor_list.html', context)

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



def mentors(request):
    # Filter users with vendor role
    mentors = CustomUser.objects.filter(role='mentor')
    
    context = {
        'mentors': mentors
    }
    return render(request, 'mentors.html', context)


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
def competition_category_list(request):
    categories = CompetitionCategory.objects.all()
    return render(request, 'competition_category_list.html', {'categories': categories})

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

def level_info(request, level_id):
    level = get_object_or_404(Level, id=level_id)
    rounds = level.rounds.all().prefetch_related("schedules")

    return render(request, "level_info.html", {
        "level": level,
        "rounds": rounds
    })

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