import base64
import datetime
import os
import pandas as pd
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt

from .models import Feature, Author
from django.contrib import messages
from io import BytesIO


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


def get_data_by_category(category, file_path):
    df = pd.read_csv(file_path)
    filtered_data = df[df['Category'] == category]

    # return filtered_data.to_dict(orient='records')
    result = filtered_data['Amount'].sum()
    return result


def insert_data_by_category(category, new_data, file_path, currency):
    # new_data = int(new_data)
    data_ = pd.read_csv(file_path)
    df = pd.DataFrame(data_)
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    new_data = pd.DataFrame([{'Date': current_date, 'Amount': new_data, 'Category': category, 'Currency': currency}])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file_path, index=False)


def data(request):
    if request.user.is_authenticated:
        file_path = os.path.join('data_files', request.user.username, 'data.csv')
        if os.path.exists(file_path):
            if request.method == 'POST':
                category = request.POST.get('category')
                new_data = request.POST['new-data']
                currency = request.POST.get('currency')
                if category and new_data:
                    insert_data_by_category(category, new_data, file_path, currency)
                else:
                    messages.error(request, f'Category or data entry is empty {category, new_data}')

                return redirect('data')
    return render(request, 'templates/data.html')


def show_graph(category, received_data):
    x = [category]
    y = [received_data]
    plt.bar(x, y)
    plt.title(f'Net Spend for {category}')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    figure = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return figure


def view_data(request):
    file_path = os.path.join('data_files', request.user.username, 'data.csv')
    received_data = None
    category = None
    if request.method == 'POST':
        category = request.POST.get('category')
        if category:
            received_data = get_data_by_category(category, file_path)
            figure = show_graph(category, received_data)
        else:
            messages.error(request, f'No category selected')
    return render(request, 'templates/view_data.html', {'received_data': received_data, 'category': category, "figure": figure})


def user_data(request):
    user_ = request.user
    # Construct the absolute path
    user_directory = os.path.join('data_files', user_.username)
    file_path = os.path.join(user_directory, 'data.csv')
    exists = os.path.exists(file_path)

    if request.method == "POST" and 'create' in request.POST:
        if not exists:
            if not os.path.exists(user_directory):
                os.makedirs(user_directory)

            return redirect('user_data')
        else:
            messages.info(request, 'File already exists')

    return render(request, 'templates/user_data.html', {'user': user_, 'file_path': exists})


def profile(request):
    posts = Author.objects.all()
    return render(request, 'templates/profile.html', {'posts': posts})
