# content_processors.py
from auth_app.models import ParticipantProfile
from admin_part.models import CompetitionCategory
from datetime import date
from django.db.models import Q

def participant_profile(request):
    if request.user.is_authenticated:
        try:
            profile = ParticipantProfile.objects.get(user=request.user)
            category = None

            if profile.age is not None:
                category = CompetitionCategory.objects.filter(
                    age_min__lte=profile.age
                ).filter(
                    Q(age_max__gte=profile.age) | Q(age_max__isnull=True)
                ).first()

            referred_name = None
            if request.user.referred_by:
                referred_name = (
                    request.user.referred_by.full_name
                    or request.user.referred_by.email
                )

            return {
                "profile": profile,
                "age": profile.age,
                "category": category.name if category else None,
                "referred_name": referred_name,   # ✅ add here
            }
        except ParticipantProfile.DoesNotExist:
            return {"profile": None, "age": None, "category": None, "referred_name": None}

    return {"profile": None, "age": None, "category": None, "referred_name": None}
