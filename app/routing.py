from django.urls import path

from .consumers import AppConsumer

websocket_urlpatterns = [
    path('ws/app/', AppConsumer)
]
