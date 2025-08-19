from django.shortcuts import render
from admin_part.models import RoundSchedule, CompetitionCategory, Level, Round,Participant
from auth_app.models import ParticipantProfile
from django.utils import timezone
from django.db.models import Q 
from datetime import datetime

# Create your views here.


def about_events(request):
    return render(request,'about_events.html')

def art_landing(request):
    countdown_ts = None
    already_participated = False

    level1 = Level.objects.filter(number=1).order_by("category__id").first()
    round1 = Round.objects.filter(level=level1, number=1).first() if level1 else None

    if request.user.is_authenticated:
        try:
            profile = ParticipantProfile.objects.get(user=request.user)
            age = profile.age
        except ParticipantProfile.DoesNotExist:
            age = None

        if age is not None and round1:
            category = CompetitionCategory.objects.filter(
                age_min__lte=age
            ).filter(
                Q(age_max__gte=age) | Q(age_max__isnull=True)
            ).first()

            if category:
                level = Level.objects.filter(category=category, number=category.level_start).first()
                round_obj = Round.objects.filter(level=level).order_by("number").first()

                # Check if user has already participated/paid
                try:
                    participant = Participant.objects.get(user=request.user, level=level, current_round=round_obj)
                    already_participated = participant.has_paid
                except Participant.DoesNotExist:
                    already_participated = False

                # If already enrolled → show competition schedule
                if already_participated:
                    schedule = RoundSchedule.objects.filter(
                        round=round_obj,
                        date__gte=timezone.localdate()
                    ).order_by("date", "start_time").first()
                    if schedule:
                        dt = timezone.make_aware(
                            datetime.combine(schedule.date, schedule.start_time)
                        )
                        countdown_ts = int(dt.timestamp() * 1000)

    # If not enrolled (or not logged in) → show last registration date instead
    if countdown_ts is None and round1 and round1.last_registration_date:
        dt = timezone.make_aware(
            datetime.combine(round1.last_registration_date, datetime.max.time())
        )
        countdown_ts = int(dt.timestamp() * 1000)

    context = {
        "countdown_ts": countdown_ts,
        "already_participated": already_participated
    }
    return render(request, "art_landing.html", context)


def art_gallery(request):
    return render(request,'art_gallery.html')



def contact_us(request):
    return render(request,'contact_us.html')

def art_contact(request):
    return render(request,'art_contact.html')


def about_us(request):
    return render(request,'about_us.html')
    


def index(request):
    return render(request,'index.html')

def comming_soon(request):
    return render(request,'comming_soon.html')

def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')


def privacy_policy(request):
    return render(request,'privacy_policy.html')

def working_on(request):
    return render(request,'working_on.html')