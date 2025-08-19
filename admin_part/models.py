from django.db import models
from django.conf import settings
from django.utils import timezone

class CompetitionCategory(models.Model):
    name = models.CharField(max_length=100)   # e.g. "Junior Artists"
    age_min = models.IntegerField()
    age_max = models.IntegerField(null=True, blank=True)  # null = no limit
    theme = models.CharField(max_length=255, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    level_start = models.IntegerField(default=1)  # Pro starts at 5
    prize_1 = models.DecimalField(max_digits=10, decimal_places=2)
    prize_2 = models.DecimalField(max_digits=10, decimal_places=2)
    prize_3 = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Level(models.Model):
    category = models.ForeignKey(CompetitionCategory, on_delete=models.CASCADE, related_name="levels")
    number = models.IntegerField()  # 1,2,3,4,5...
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Level {self.number} - {self.category.name}"


class Round(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="rounds")
    number = models.IntegerField()  # 1,2,3
    mode = models.CharField(max_length=20, choices=[("online", "Online"), ("offline", "Offline")])
    description = models.TextField(blank=True, null=True)
    last_registration_date = models.DateField(
        null=True,
        blank=True,
        help_text="Last date for registration for this round"
    )
    def __str__(self):
        return f"Level {self.level.number} - Round {self.number} ({self.mode})"

class Participant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField()
    category = models.ForeignKey("CompetitionCategory", on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey("Level", on_delete=models.SET_NULL, null=True, blank=True)
    current_round = models.ForeignKey("Round", on_delete=models.SET_NULL, null=True, blank=True)

    # ✅ Track payment status
    has_paid = models.BooleanField(default=False)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.get_full_name()


class ParticipantPayment(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="payments")
    
    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    # Amount details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=[("created", "Created"), ("paid", "Paid"), ("failed", "Failed")],
        default="created"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    def mark_as_paid(self, razorpay_payment_id, signature=None):
        self.status = "paid"
        self.razorpay_payment_id = razorpay_payment_id
        self.razorpay_signature = signature
        self.payment_date = timezone.now()
        self.save()

        # ✅ also update participant
        self.participant.has_paid = True
        self.participant.total_paid += self.amount
        self.participant.save()

    def __str__(self):
        return f"{self.participant.user.get_full_name()} - {self.amount} ({self.status})"


class RoundSchedule(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="schedules")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_seats = models.IntegerField(default=0)
    booked_seats = models.IntegerField(default=0)

    def available_seats(self):
        return self.total_seats - self.booked_seats

    def __str__(self):
        return f"{self.round} - {self.date} ({self.start_time} to {self.end_time})"
