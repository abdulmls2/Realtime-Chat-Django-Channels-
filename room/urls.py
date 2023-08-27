from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_rooms, name='user_rooms'),
    path('<slug:slug>/', views.room, name='room'),
]