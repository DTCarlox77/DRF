from django.urls import path
from .consumers import NotificacionesConsumer

websocket_urlpatterns = [
    path(r'ws/notificaciones/<int:id>', NotificacionesConsumer.as_asgi())
]