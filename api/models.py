from django.db import models

# Create your models here.
class Song(models.Model):
    
    name = models.CharField(max_length=50)
    artist = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f'Canción: {self.name}, por: {self.artist}'