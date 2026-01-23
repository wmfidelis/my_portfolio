from django.contrib import admin
from .models import (DailyCheckIn, AffirmationCategory, Affirmation, GratitudeEntry,
                     MeditationSession, Resource, CommunityPost, CommunityPostLike)

@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'morning_mood', 'evening_mood', 'prayed', 'meditated']
    list_filter = ['date', 'morning_mood', 'prayed', 'meditated']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'date'

@admin.register(AffirmationCategory)
class AffirmationCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']

@admin.register(Affirmation)
class AffirmationAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'category', 'author', 'is_active', 'created_date']
    list_filter = ['category', 'is_active', 'created_date']
    search_fields = ['text', 'author']
    list_editable = ['is_active']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Affirmation'

@admin.register(GratitudeEntry)
class GratitudeEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'entry_preview', 'created_date']
    list_filter = ['date']
    search_fields = ['user__username', 'entry']
    date_hierarchy = 'date'
    
    def entry_preview(self, obj):
        return obj.entry[:50] + '...' if len(obj.entry) > 50 else obj.entry
    entry_preview.short_description = 'Entry'

@admin.register(MeditationSession)
class MeditationSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'duration_minutes', 'date']
    list_filter = ['session_type', 'date']
    search_fields = ['user__username', 'notes']
    date_hierarchy = 'date'

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'is_crisis_support', 'is_featured']
    list_filter = ['resource_type', 'is_crisis_support', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['is_crisis_support', 'is_featured']

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'author', 'is_anonymous', 'is_approved', 'likes_count', 'created_date']
    list_filter = ['is_anonymous', 'is_approved', 'created_date']
    search_fields = ['author__username', 'display_name', 'content']
    list_editable = ['is_approved']
    readonly_fields = ['likes_count', 'created_date']
    date_hierarchy = 'created_date'

@admin.register(CommunityPostLike)
class CommunityPostLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_date']
    list_filter = ['created_date']
    search_fields = ['user__username']