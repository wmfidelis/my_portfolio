from django.contrib import admin
from .models import Project, Skill, ContactMessage

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_filter = ['category']
    search_fields = ['name']
    list_editable = ['proficiency', 'order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'created_date', 'order']
    list_filter = ['is_featured', 'created_date']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'order']
    filter_horizontal = ['technologies']
    date_hierarchy = 'created_date'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_date', 'is_read']
    list_filter = ['is_read', 'created_date']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_date']
    date_hierarchy = 'created_date'