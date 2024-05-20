from .models import Song
from .serializers import SongSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class SongView(APIView):
    
    http_method_names = ['get', 'post']
    
    def get(self, request):
        
        songs = Song.objects.all()
        serialized_songs = SongSerializer(songs, many=True)
        
        return Response(serialized_songs.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)