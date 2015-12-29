from django.contrib import admin

# Register your models here.
from competitions.models import (
    Competition,
    Event,
    EventLocation,
    Judge,
    Athlete,
    ScoringStation,
)

class ScoringStationInline(admin.TabularInline):
    model = ScoringStation
    ordering = ("station_num",)
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [ScoringStationInline]
    list_display = ('name', 'scheduled_start_datetime', 'competition')
    list_filter = ['competition']
    exclude = ('timer',)
    ordering = ("scheduled_start_datetime",)

class JudgeAdmin(admin.ModelAdmin):
    ordering = ("name",)

class AthleteAdmin(admin.ModelAdmin):
    ordering = ("name",)

admin.site.register(Competition)
admin.site.register(EventLocation)
admin.site.register(Event, EventAdmin)
admin.site.register(Judge, JudgeAdmin)
admin.site.register(Athlete, AthleteAdmin)
