import random
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from .models import Feature,Author
from django.contrib import messages
import requests

OPEN_WEATHER_WEBSITE = 'https://api.openweathermap.org/data/2.5/weather'

API_KEY = '9c4105c6d77a231031727bbe25190291'


def index(request):
    features = Feature.objects.all()
    return render(request, 'templates/index.html', {'features': features})


def register(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password_2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use')
                return redirect('register')
            elif User.objects.filter(username=name).exists():
                messages.error(request, 'Username already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(name, email, password)
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match, try again')
            return redirect('register')
    return render(request, 'templates/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')  # Redirect to the index view
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')
    return render(request, 'templates/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def post(request, pk):
    posts = Author.objects.get(pk=pk)
    return render(request, 'templates/post.html', {'posts': posts})


def profile(request):
    posts = Author.objects.all()
    return render(request, 'templates/profile.html', {'posts': posts})


# def weather(request, latitude, longitude):
#     try:
#         params = {
#             'lat': latitude,
#             'lon': longitude,
#             'appid': API_KEY,
#             'units': 'metric'
#         }
#         response = requests.get(OPEN_WEATHER_WEBSITE, params=params)
#         response.raise_for_status()
#         data = response.json()
#         temp = data['main']['temp']
#         weather_ = data['weather']
#         if response.status_code == 200:
#             weather_data = {
#                 'temperature': temp,
#                 'description': weather_['description'],
#             }
#             return render(request, 'templates/weather.html', {'data': weather_data})
#     except Exception as e:
#         messages.error(request, f"Request error: {e}")
#         return redirect('submit')


# def submit(request):
#     if request.method == 'POST':

        # if lat and lon:
        #     return redirect('weather', latitude=lat, longitude=lon)
        # else:
        #     messages.error(request, 'Latitude and Longitude are required')
        #     return render(request, 'templates/submit.html')
    # return render(request, 'templates/submit.html')

