from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('camera', livefe, name='camera'),
    path('get-emotions/', get_emotions, name='get_emotions'),
]
