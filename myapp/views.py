import datetime
import random

import pandas as pd
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt

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


def get_data_by_category(category):

    file = 'data_files/data.csv'
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    target_month = datetime.datetime.today().month
    filtered_data = df[(df['Date'].dt.month == target_month) & (df['Category'] == category)]
    if not filtered_data.empty:
        actual_data = filtered_data['Amount'].sum()
        return f'Total amount spent for {category} in {datetime.datetime.today().strftime("%B")} is {actual_data} Tenge'
    return filtered_data


def data(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        if category:
            actual_data = get_data_by_category(category)
        else:
            actual_data = 'No Category Selected'
    else:
        actual_data = 'No Data Available'
    return render(request, 'templates/data.html', {'data': actual_data})




def profile(request):
    posts = Author.objects.all()
    return render(request, 'templates/profile.html', {'posts': posts})
