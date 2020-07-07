from django.urls import path

from . import views_old

app_name = 'foodie_friend_app'

urlpatterns = [
    path('', views_old.home, name='home'),
]