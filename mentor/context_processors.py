# context_processors.py

from auth_app.models import MentorProfile

def mentor_profile(request):
    """Adds the mentor/vendor profile to templates if the user is a mentor or vendor."""
    if request.user.is_authenticated and getattr(request.user, "role", None) in ["mentor", "vendor"]:
        profile = MentorProfile.objects.filter(user=request.user).first()
        return {"mentor_profile": profile}
    return {"mentor_profile": None}
