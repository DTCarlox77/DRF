from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Song
        fields = '__all__'
        
    def validate_name(self, value):
        
        if Song.objects.filter(name=value).exists():
            raise serializers.ValidationError('El nombre ya existe.')
        return value
    
    def validate_image(self, value):
        
        if not (value.startswith('http://') or value.startswith('https://')):
            raise serializers.ValidationError("La URL de imagen no es válida.")
        return value