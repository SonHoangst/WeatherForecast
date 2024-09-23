from django.contrib import admin
from django.urls import path 
from .views import weather_view
from . import views 

urlpatterns = [
    # path('', weather_view, name='weather_dashboard'),
    path('', views.weather_view, name='dashboard'),
    path('subscribe/', views.subscribe_view, name="subscribe"), 
]
