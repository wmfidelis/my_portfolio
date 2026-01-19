from django.contrib import admin
from .models import Post, Category, Tag, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_date']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_date']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'published_date']
    list_filter = ['status', 'is_featured', 'category', 'created_date', 'published_date']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views', 'created_date', 'updated_date']
    date_hierarchy = 'published_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Classification', {
            'fields': ('tags', 'status', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('views', 'created_date', 'updated_date', 'published_date'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_approved', 'created_date', 'is_reply']
    list_filter = ['is_approved', 'created_date']
    search_fields = ['author__username', 'post__title', 'content']
    list_editable = ['is_approved']
    readonly_fields = ['created_date', 'updated_date']
    date_hierarchy = 'created_date'