from django.contrib import admin
from vacancies.models import Vacancy


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'is_participant', 'is_priority', 'created']
    list_editable = ['is_participant', 'is_priority']

admin.site.register(Vacancy, VacancyAdmin)
