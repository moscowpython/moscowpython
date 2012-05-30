from django.contrib import admin
from meetup.models import Talk, Sponsor, Speaker, Event


class TalkAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'speaker', 'event']
    list_filter = ['event']


class EventAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'date']


class SpeakerAdmin(admin.ModelAdmin):
    pass


class SponsorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Talk, TalkAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Sponsor, SpeakerAdmin)