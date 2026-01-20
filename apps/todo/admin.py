from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'status', 'due_date', 'is_overdue', 'created_date']
    list_filter = ['status', 'priority', 'created_date', 'due_date']
    search_fields = ['title', 'description', 'user__username']
    list_editable = ['status', 'priority']
    readonly_fields = ['created_date', 'updated_date', 'completed_date']
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'user')
        }),
        ('Task Details', {
            'fields': ('priority', 'status', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date', 'completed_date'),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
    
    actions = ['mark_completed', 'mark_in_progress', 'mark_todo']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} task(s) marked as completed.')
    mark_completed.short_description = 'Mark selected tasks as completed'
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} task(s) marked as in progress.')
    mark_in_progress.short_description = 'Mark selected tasks as in progress'
    
    def mark_todo(self, request, queryset):
        updated = queryset.update(status='todo')
        self.message_user(request, f'{updated} task(s) marked as to do.')
    mark_todo.short_description = 'Mark selected tasks as to do'