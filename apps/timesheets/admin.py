from django.contrib import admin
from apps.timesheets.models import ClientRateCard, WeeklyTimesheet, TimesheetEntry

@admin.register(ClientRateCard)
class ClientRateCardAdmin(admin.ModelAdmin):
    list_display = ('project', 'role_name', 'hourly_billable_rate', 'currency')

@admin.register(WeeklyTimesheet)
class WeeklyTimesheetAdmin(admin.ModelAdmin):
    list_display = ('employee', 'week_start_date', 'total_billable_hours', 'status')
    list_filter = ('status',)

@admin.register(TimesheetEntry)
class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ('timesheet', 'project', 'entry_date', 'hours_logged', 'is_billable')
