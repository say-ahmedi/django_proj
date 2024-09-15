from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('post/<str:pk>', views.post, name='post'),

    path('profile/', views.profile, name='profile'),

    path('data/', views.data, name='data'),

    path('user_data/', views.user_data, name='user_data'),

    path('retrieve_data/', views.retrieve_data, name='retrieve_data'),
]
