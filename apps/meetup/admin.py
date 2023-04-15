from __future__ import annotations

from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import EventAdminForm
from .models import Event, Executive, MediaCoverage, Photo, Speaker, Sponsor, Talk, Tutorial, Venue, Vote


@admin.display(description='Слайды', boolean=True)
def oembed_presentation(obj):
    return bool(obj.presentation_data)


@admin.display(description='Видео', boolean=True)
def oembed_video(obj):
    return bool(obj.video_data)


def preview(obj):
    return mark_safe(f'<img src="{obj.get_absolute_url()}" style="height:100px">')


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'position', 'speaker', 'status', oembed_presentation, oembed_video, 'event']
    list_editable = ['position']
    list_filter = ['event']
    readonly_fields = ['presentation_data', 'video_data']
    search_fields = ['name']
    ordering = ['-event__pk', 'position']


class PhotoInline(admin.TabularInline):
    model = Photo


class MediaCoverageInline(admin.TabularInline):
    model = MediaCoverage


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ['__str__', 'date', 'venue', 'status']
    list_editable = ['status']
    exclude = ['status_changed']
    inlines = [PhotoInline, MediaCoverageInline]


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'address']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['__str__', preview, 'event', 'caption']
    list_editable = ['caption']
    list_per_page = 10
    ordering = ['-id']


def photo_preview(obj):
    return mark_safe(f'<img src="{obj.avatar_url}" style="height:50px">')


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['__str__', photo_preview, 'slug']
    list_editable = ['slug']
    search_fields = ['name']


def logo_preview(obj):
    return mark_safe(f'<img src="{obj.logo.url}" width=150>')


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['__str__', logo_preview, 'url']
    list_editable = ['url']


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    pass


@admin.register(MediaCoverage)
class MediaCoverageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'event']
    list_filter = ['event']
    ordering = ['-event__pk', 'id']


admin.site.register(Vote)
admin.site.register(Executive)
