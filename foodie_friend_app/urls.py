from django.urls import path

from . import views

app_name = 'foodie_friend_app'

urlpatterns = [
    path('', views.home, name='home'),
]