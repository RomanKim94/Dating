from django.contrib import admin
from django.urls import path, include

from .views import PersonCreateViewSet

urlpatterns = [
    path('create/', PersonCreateViewSet.as_view({'post': 'create'}))
]
