# context_processors.py

from auth_app.models import MentorProfile

def mentor_profile(request):
    if request.user.is_authenticated and getattr(request.user, "role", None) in ["mentor", "vendor"]:
        profile = MentorProfile.objects.filter(user=request.user).first()
        if profile:
            return {"mentor_profile": profile}
    return {"mentor_profile": request.user}  # fallback
