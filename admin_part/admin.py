from django.contrib import admin
from .models import CompetitionCategory, Level, Round, Participant,RoundSchedule


class RoundInline(admin.TabularInline):
    model = Round
    extra = 1   # how many empty forms to display
    fields = ("number", "mode", "description")
    ordering = ("number",)


class LevelInline(admin.TabularInline):
    model = Level
    extra = 1
    fields = ("number", "description")
    ordering = ("number",)


@admin.register(CompetitionCategory)
class CompetitionCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "age_min", "age_max", "theme", "fee", "level_start")
    list_filter = ("level_start",)
    search_fields = ("name", "theme")
    inlines = [LevelInline]  # show levels inline


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("number", "category", "description")
    list_filter = ("category",)
    search_fields = ("description",)
    inlines = [RoundInline]  # show rounds inline


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("number", "mode", "level", "description")
    list_filter = ("mode", "level__category")
    search_fields = ("description",)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "age", "category", "level", "current_round")
    list_filter = ("category", "level")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")


@admin.register(RoundSchedule)
class RoundScheduleAdmin(admin.ModelAdmin):
    list_display = ("round", "date", "start_time", "end_time", "total_seats", "booked_seats", "available_seats")
    list_filter = ("date", "round__level__category")
    search_fields = ("round__level__category__name", "round__level__number", "round__number")
    ordering = ("date", "start_time")

    def available_seats(self, obj):
        return obj.available_seats()
    available_seats.short_description = "Available Seats"