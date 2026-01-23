from django.urls import path
from . import views

app_name = 'hope_healing'

urlpatterns = [
    path('', views.index, name='index'),
    path('checkin/', views.daily_checkin, name='daily_checkin'),
    path('affirmations/', views.affirmations, name='affirmations'),
    path('gratitude/', views.gratitude_journal, name='gratitude_journal'),
    path('meditation/', views.meditation_timer, name='meditation_timer'),
    path('progress/', views.progress_dashboard, name='progress_dashboard'),
    path('resources/', views.resources, name='resources'),
    path('community/', views.community, name='community'),
    path('community/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]