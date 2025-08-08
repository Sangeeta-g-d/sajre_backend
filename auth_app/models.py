from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from datetime import date
import uuid
from datetime import timedelta


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('driver', 'Driver'),
        ('employee', 'Employee'),
        ('customer', 'Customer'),
        ('participant', 'Participant'),
        ('mentor', 'Mentor'),
        ('teacher', 'Teacher'),
        ('school', 'School'),
        ('college', 'College'),
        ('vendor', 'Vendor'),
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    accepted_terms = models.BooleanField(default=False)

    # Referral System
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey(
        "self",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="referrals"
    )

    # Default Django fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.referral_code:
            # Generate a unique referral code (first 8 chars of UUID)
            self.referral_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)


class UserOTP(models.Model):
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)  # OTP valid 5 mins
    
class ParticipantProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="participant_profile"
    )

    # Personal Details
    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    full_address = models.TextField(blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    # File uploads
    dob_proof = models.FileField(upload_to="participants/dob_proofs/", blank=True, null=True)
    photo = models.ImageField(upload_to="participants/photos/", blank=True, null=True)
    edu_doc = models.FileField(upload_to="participants/education_docs/", blank=True, null=True)

    # Referral & Marketing
    how_did_you_know = models.CharField(max_length=100, blank=True, null=True)
    referral_code_used = models.CharField(max_length=10, blank=True, null=True)  # ✅ the code they entered

    # Education Details
    school_name = models.CharField(max_length=255, blank=True, null=True)
    school_board = models.CharField(max_length=100, blank=True, null=True)
    school_location = models.CharField(max_length=255, blank=True, null=True)

    course_name = models.CharField(max_length=255, blank=True, null=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    university_name = models.CharField(max_length=255, blank=True, null=True)
    academic_year = models.CharField(max_length=50, blank=True, null=True)
    stream = models.CharField(max_length=100, blank=True, null=True)

    # Age (calculated from dob)
    age = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Participant Profile - {self.user.email}"

    def calculate_age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super().save(*args, **kwargs)


class MentorProfile(models.Model):
    QUALIFICATION_CHOICES = [
        ("PhD", "PhD"),
        ("Master's Degree", "Master's Degree"),
        ("Bachelor's Degree", "Bachelor's Degree"),
        ("Diploma", "Diploma"),
        ("Other", "Other"),
    ]

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="mentor_profile"
    )

    # Step 1: Qualification Details
    higher_qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    passport_photo = models.ImageField(upload_to="mentors/passport_photos/")
    id_proof = models.FileField(upload_to="mentors/id_proofs/")

    full_address = models.TextField()
    store_or_advisor = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    course_level = models.CharField(max_length=255)  # e.g., "PhD"
    course_name = models.CharField(max_length=255)

    # Step 2: Professional Details
    job_title = models.CharField(max_length=255)
    total_experience_years = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    work_history = models.TextField(blank=True, null=True)
    current_employer = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentor Profile - {self.user.full_name or self.user.email}"