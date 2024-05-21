from django.urls import path
from .views import SongView, SongDetailView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path('songs/', SongView.as_view(), name='songs'),
    path('songs/<int:id>', SongDetailView.as_view(), name='songs-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
