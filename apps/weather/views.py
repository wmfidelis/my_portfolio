from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
import requests
from datetime import datetime

OPENWEATHER_API_KEY = settings.OPENWEATHER_API_KEY
BASE_URL = "https://api.openweathermap.org/data/2.5"

def get_weather_data(city):
    """Fetch current weather data from OpenWeatherMap API"""
    cache_key = f'weather_{city.lower()}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        url = f"{BASE_URL}/weather"
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'  # Use Celsius
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process and structure the data
        weather_data = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'temp_min': round(data['main']['temp_min']),
            'temp_max': round(data['main']['temp_max']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
            'clouds': data['clouds']['all'],
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
            'visibility': data.get('visibility', 0) / 1000,  # Convert to km
            'coord': data['coord'],
        }
        
        # Cache for 30 minutes
        cache.set(cache_key, weather_data, 1800)
        
        return weather_data
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {'error': 'City not found. Please check the spelling and try again.'}
        else:
            return {'error': f'API Error: {e.response.status_code}'}
    except requests.exceptions.RequestException as e:
        return {'error': 'Unable to connect to weather service. Please try again later.'}
    except Exception as e:
        return {'error': 'An unexpected error occurred. Please try again.'}


def get_forecast_data(city):
    """Fetch 5-day weather forecast from OpenWeatherMap API"""
    cache_key = f'forecast_{city.lower()}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        url = f"{BASE_URL}/forecast"
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process forecast data - get one forecast per day at noon
        daily_forecasts = []
        processed_dates = set()
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            hour = datetime.fromtimestamp(item['dt']).hour
            
            # Get forecast around noon (12:00) for each day
            if date not in processed_dates and 11 <= hour <= 13:
                forecast = {
                    'date': datetime.fromtimestamp(item['dt']).strftime('%a, %b %d'),
                    'temperature': round(item['main']['temp']),
                    'temp_min': round(item['main']['temp_min']),
                    'temp_max': round(item['main']['temp_max']),
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': round(item['wind']['speed'] * 3.6, 1),
                }
                daily_forecasts.append(forecast)
                processed_dates.add(date)
                
                if len(daily_forecasts) >= 5:
                    break
        
        # Cache for 1 hour
        cache.set(cache_key, daily_forecasts, 3600)
        
        return daily_forecasts
    
    except Exception as e:
        return []


def index(request):
    """Main weather page"""
    weather_data = None
    forecast_data = None
    city = request.GET.get('city', '').strip()
    
    # Default cities to suggest
    default_cities = [
        'Nairobi', 'London', 'New York', 'Tokyo', 
        'Paris', 'Sydney', 'Dubai', 'Singapore'
    ]
    
    if city:
        # Get current weather
        weather_data = get_weather_data(city)
        
        if 'error' in weather_data:
            messages.error(request, weather_data['error'])
            weather_data = None
        else:
            # Get forecast if current weather is successful
            forecast_data = get_forecast_data(city)
            if not forecast_data:
                messages.warning(request, 'Forecast data is currently unavailable.')
    
    context = {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'city': city,
        'default_cities': default_cities,
    }
    
    return render(request, 'weather/index.html', context)


def quick_weather(request, city):
    """Quick weather lookup for a specific city"""
    weather_data = get_weather_data(city)
    
    if 'error' in weather_data:
        messages.error(request, weather_data['error'])
        return render(request, 'weather/index.html', {
            'default_cities': ['Nairobi', 'London', 'New York', 'Tokyo']
        })
    
    forecast_data = get_forecast_data(city)
    
    context = {
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'city': city,
        'default_cities': ['Nairobi', 'London', 'New York', 'Tokyo', 'Paris', 'Sydney'],
    }
    
    return render(request, 'weather/index.html', context)