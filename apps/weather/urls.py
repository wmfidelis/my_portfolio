from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('city/<str:city>/', views.quick_weather, name='quick_weather'),
]