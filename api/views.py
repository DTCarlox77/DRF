from .models import Song
from .serializers import SongSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class SongView(APIView):
    http_method_names = ['get', 'post']
    pagination_class = CustomPageNumberPagination
    
    def get(self, request):
        
        if request.query_params:
            keyword = request.query_params.get('keyword', None)
            limit = int(request.query_params.get('limit', 0))
        
            if keyword:
                songs = Song.objects.filter(artist__icontains=keyword)[:limit]
            else:
                songs = Song.objects.all()[:limit]

        paginator = self.pagination_class()
        songs = Song.objects.all()
        result_page = paginator.paginate_queryset(songs, request)

        serializer = SongSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SongDetailView(APIView):
    
    http_method_names = ['get', 'put', 'patch']
    
    def get(self, request, id):
        
        try:
            
            song = Song.objects.get(id=id)
            serialized_song = SongSerializer(song)
            return Response(serialized_song.data, status=status.HTTP_200_OK)
        
        except Song.DoesNotExist:
            
            return Response({'message': 'No se han encontrado coincidencias'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, id):
        
        try:
            
            song = Song.objects.get(id=id)
        
        except Song.DoesNotExist:
            
            return Response({'message': 'No se han encontrado coincidencias'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SongSerializer(song, data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, id):
        
        try:
            
            song = Song.objects.get(id=id)
        
        except Song.DoesNotExist:
            
            return Response({'message': 'No se han encontrado coincidencias'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SongSerializer(song, data=request.data, partial=True)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)