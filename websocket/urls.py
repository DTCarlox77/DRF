from django.urls import path
from django.conf.urls import include
from .routing import websocket_urlpatterns
from .views import main

urlpatterns = [
    path('', include(websocket_urlpatterns)),
    path('sala/<int:id>/', main, name='main')
]
