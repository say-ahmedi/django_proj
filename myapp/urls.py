from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('post/<str:pk>', views.post, name='post'),

    path('profile/', views.profile, name='profile'),

    path('data/', views.data, name='data'),

    path('user_data/', views.user_data, name='user_data'),

    path('view_data/', views.view_data, name='view_data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)