from django.shortcuts import render
import requests
import datetime


def index(request):
    api_key = open("C:\\Users\\amanr\\PycharmProjects\\Project\\Current Project\\API_KEY", "r").read()
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }
        data1 = {
            "city": context['weather_data1']['city'],
            "temperature": str(context['weather_data1']['temperature']) + "°C",
            "desc": context['weather_data1']['description'],
            "icon": context['weather_data1']['icon'],

            "day1": daily_forecasts1[0]['day'],
            "min_temp1": str(daily_forecasts1[0]['min_temp']) + "°C",
            "desc1": daily_forecasts1[0]['description'],
            "f_icon1": daily_forecasts1[0]['icon'],

            "day2": daily_forecasts1[1]['day'],
            "min_temp2": str(daily_forecasts1[1]['min_temp']) + "°C",
            "desc2": daily_forecasts1[1]['description'],
            "f_icon2": daily_forecasts1[1]['icon'],

            "day3": daily_forecasts1[2]['day'],
            "min_temp3": str(daily_forecasts1[2]['min_temp']) + "°C",
            "desc3": daily_forecasts1[2]['description'],
            "f_icon3": daily_forecasts1[2]['icon'],

            "day4": daily_forecasts1[3]['day'],
            "min_temp4": str(daily_forecasts1[3]['min_temp']) + "°C",
            "desc4": daily_forecasts1[3]['description'],
            "f_icon4": daily_forecasts1[3]['icon'],

            "day5": daily_forecasts1[4]['day'],
            "min_temp5": str(daily_forecasts1[4]['min_temp']) + "°C",
            "desc5": daily_forecasts1[4]['description'],
            "f_icon5": daily_forecasts1[4]['icon'],
        }
        data2 = {}
        if(weather_data2):
            data2 = {
                "city": context['weather_data2']['city'],
                "temperature": str(context['weather_data2']['temperature']) + "°C",
                "desc": context['weather_data2']['description'],
                "icon": context['weather_data2']['icon'],

                "day": daily_forecasts2[0]['day'],
                "min_temp": str(daily_forecasts2[0]['min_temp']) + "°C",
                "desc": daily_forecasts2[0]['description'],
                "f_icon": daily_forecasts2[0]['icon'],

                "day2": daily_forecasts2[1]['day'],
                "min_temp2": str(daily_forecasts2[1]['min_temp']) + "°C",
                "desc2": daily_forecasts2[1]['description'],
                "f_icon2": daily_forecasts2[1]['icon'],

                "day3": daily_forecasts2[2]['day'],
                "min_temp3": str(daily_forecasts2[2]['min_temp']) + "°C",
                "desc3": daily_forecasts2[2]['description'],
                "f_icon3": daily_forecasts2[2]['icon'],

                "day4": daily_forecasts2[3]['day'],
                "min_temp4": str(daily_forecasts2[3]['min_temp']) + "°C",
                "desc4": daily_forecasts2[3]['description'],
                "f_icon4": daily_forecasts2[3]['icon'],

                "day5": daily_forecasts2[4]['day'],
                "min_temp5": str(daily_forecasts2[4]['min_temp']) + "°C",
                "desc5": daily_forecasts2[4]['description'],
                "f_icon5": daily_forecasts2[4]['icon'],
            }

        return render(request, 'index.html', {'abc1': data1, 'abc2': data2})
    else:
        return render(request, 'index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lon, lat = response['coord']['lon'], response['coord']['lat']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            'description': daily_data['weather'][0]['description'],
            'icon': daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
