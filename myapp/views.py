import random
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from .models import Feature,Author
from django.contrib import messages


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
    return render(request, 'templates/post.html', {'posts':posts})


def counter(request):
    posts = Author.objects.all()
    return render(request, 'templates/profile.html', {'posts': posts})
