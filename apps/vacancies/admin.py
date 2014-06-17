from django.contrib import admin
from .models import Vacancy


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'salary', 'is_participant', 'is_priority', 'created']
    list_editable = ['is_participant', 'is_priority']


admin.site.register(Vacancy, VacancyAdmin)
