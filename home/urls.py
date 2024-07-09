from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("carContainers/", views.carContainers, name='car'),
    path("requestCombinations/", views.requestCombinations, name='requestCombinations')
]
