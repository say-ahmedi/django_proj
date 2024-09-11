from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('post/<str:pk>', views.post, name='post'),

    path('profile/', views.profile, name='profile'),

    path('weather/<str:latitude>/<str:longitude>/', views.weather, name='weather'),

    path('submit/', views.submit, name='submit'),

    # path('search/', views.search, name='search')
]
