# coding: utf-8
from django.contrib import admin
from .forms import EventAdminForm
from .models import Photo, Venue, MediaCoverage, Talk, Sponsor, Speaker, \
    Event, Tutorial, Vote


def oembed_presentation(obj):
    return bool(obj.presentation_data)
oembed_presentation.short_description = u'Слайды'
oembed_presentation.boolean = True


def oembed_video(obj):
    return bool(obj.video_data)
oembed_video.short_description = u'Видео'
oembed_video.boolean = True


def preview(obj):
    return '<img src=%s style="height:100px">' % obj.get_absolute_url()
preview.allow_tags = True


class TalkAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'position', 'speaker', 'status', oembed_presentation, oembed_video, 'event']
    list_editable = ['position']
    list_filter = ['event']
    readonly_fields = ['presentation_data', 'video_data']
    ordering = ['-event__pk', 'position']


class PhotoInline(admin.TabularInline):
    model = Photo


class MediaCoverageInline(admin.TabularInline):
    model = MediaCoverage


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ['__unicode__', 'date', 'venue', 'status']
    list_editable = ['status']
    exclude = ['status_changed']
    inlines = [PhotoInline, MediaCoverageInline]


class VenueAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'address']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', preview, 'event', 'caption']
    list_editable = ['caption']
    list_per_page = 10
    ordering = ['-id']


def photo_preview(obj):
    return '<img src=%s style="height:50px">' % obj.avatar_url
photo_preview.allow_tags = True


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', photo_preview, 'slug',]
    list_editable = ['slug']


def logo_preview(obj):
    return '<img src=%s width=150>' % obj.logo.url
logo_preview.allow_tags = True


class SponsorAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', logo_preview, 'url',]
    list_editable = ['url']


class TutorialAdmin(admin.ModelAdmin):
    pass


class MediaCoverageAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'event']
    list_filter = ['event']
    ordering = ['-event__pk', 'id']


admin.site.register(Talk, TalkAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(MediaCoverage, MediaCoverageAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Vote)
