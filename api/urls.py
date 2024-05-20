from django.urls import path
from .views import SongView, SongDetailView

urlpatterns = [
    path('songs/', SongView.as_view(), name='songs'),
    path('songs/<int:id>', SongDetailView.as_view(), name='songs-detail')
]
