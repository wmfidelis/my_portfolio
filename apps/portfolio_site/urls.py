from django.urls import path
from . import views

app_name = 'portfolio_site'

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
]