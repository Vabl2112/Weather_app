import requests
from django.shortcuts import render
from datetime import datetime
from dadata import Dadata


def index(request):
    api_key = 'c9672730-f400-4301-9415-489548edbe33'
    url_geocoder = 'https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode={}&results=1&format=json'
    url_current_weather = 'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m,apparent_temperature,wind_speed_10m,precipitation&timezone=auto'
    url_forecast_weather = 'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&hourly=temperature_2m,apparent_temperature,wind_speed_10m,precipitation&forecast_days=3&timezone=auto'

    if request.method == 'POST':
        city = request.POST['city']

        current_weather, forecast_weather = find_current_and_forecast_weather(city, api_key, url_geocoder,
                                                                              url_current_weather, url_forecast_weather)

        context = {
            'current_weather': current_weather,
            'forecast_weather': forecast_weather,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')



def find_date_name(date):
    date_object = datetime.fromisoformat(date)
    day_of_week = date_object.weekday()
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return days[day_of_week]


def make_time(date):
    date = date.split('T')
    return date[1]


def find_current_and_forecast_weather(city, api_key, url_geocoder, url_current_weather, url_forecast_weather):
    geocoder = requests.get(url_geocoder.format(api_key, city)).json()
    location = geocoder['response']['GeoObjectCollection']["featureMember"][0]["GeoObject"]["name"]
    geo = geocoder['response']['GeoObjectCollection']["featureMember"][0]["GeoObject"]["Point"]['pos'].split()
    lat, lon = geo[1], geo[0]
    current_info = requests.get(url_current_weather.format(lat, lon)).json()
    forecast_info = requests.get(url_forecast_weather.format(lat, lon)).json()
    current_weather = {
        'location': location,
        'temperature': round(current_info['current']['temperature_2m']),
        'apparent_temperature': round(current_info['current']['apparent_temperature']),
        'wind': current_info['current']['wind_speed_10m'],
        'precipitation': current_info['current']['precipitation'],
    }

    forecast_weather = [[], [], []]
    for hourly_data in range(2, 72, 3):
        data_weather = {
            'week': find_date_name(forecast_info['hourly']['time'][hourly_data]),
            'time': make_time(forecast_info['hourly']['time'][hourly_data]),
            'temperature': round(forecast_info['hourly']['temperature_2m'][hourly_data]),
            'apparent_temperature': round(forecast_info['hourly']['apparent_temperature'][hourly_data]),
            'wind': forecast_info['hourly']['wind_speed_10m'][hourly_data],
            'precipitation': forecast_info['hourly']['precipitation'][hourly_data],
        }
        if hourly_data < 24:
            forecast_weather[0].append(data_weather)
        elif hourly_data < 48:
            forecast_weather[1].append(data_weather)
        else:
            forecast_weather[2].append(data_weather)

    return current_weather, forecast_weather
