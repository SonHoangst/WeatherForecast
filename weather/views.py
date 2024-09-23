import requests
from django.shortcuts import render
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
from django.shortcuts import redirect
from .forms import SubscriptionForm
from .models import Subscription

API_KEY = '1e7f8a349ee447ddaa821629242109'

def get_weather_data(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=5"
    response = requests.get(url)
    return response.json()

def weather_view(request):
    city = request.GET.get('city', 'London')  # Default to London
    data = get_weather_data(city)
    
    current_weather = {
        'city': data['location']['name'],
        'country': data['location']['country'],
        'temperature': data['current']['temp_c'],
        'wind_speed': data['current']['wind_kph'],
        'humidity': data['current']['humidity'],
        'condition': data['current']['condition']['text'],
    }

    forecast = [
        {
            'date': datetime.strptime(forecast['date'], '%Y-%m-%d').strftime('%d-%m-%Y'),
            'temp': forecast['day']['avgtemp_c'],
            'wind': forecast['day']['maxwind_kph'],
            'humidity': forecast['day']['avghumidity'],
            'condition': forecast['day']['condition']['text'],
        } for forecast in data['forecast']['forecastday']
    ]
    
    return render(request, 'app/dashboard.html', {
        'current_weather': current_weather,
        'forecast': forecast
    })


def send_weather_email(email, weather_info):
    subject = f"Daily Weather Forecast for {weather_info['city']}"
    message = (
        f"Here is the daily forecast for {weather_info['city']}:\n"
        f"Temperature: {weather_info['temperature']}°C\n"
        f"Humidity: {weather_info['humidity']}%\n"
        f"Wind Speed: {weather_info['wind_speed']} KPH\n"
        f"Condition: {weather_info['condition']}\n"
        "Have a great day!"
    )
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        print(f"Weather email sent successfully to {email}")
    except SMTPException as e:
        print(f"Error sending email to {email}: {e}")


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Save the subscription
            subscription = form.save()

            # Optionally, send a confirmation email after successful subscription
            send_weather_email(subscription.email, {
                'city': subscription.city,
                'temperature': 'N/A',  # For demo purposes
                'humidity': 'N/A',
                'wind_speed': 'N/A',
                'condition': 'N/A',
            })

            return redirect('weather_dashboard')
    else:
        form = SubscriptionForm()

    return render(request, 'app/subscribe.html', {'form': form})
