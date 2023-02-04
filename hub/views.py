from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Club
from .serializers import *

@api_view(['GET', 'POST'])
def clubs_list(request, school):
    if request.method == 'GET':
        data = Club.objects.filter(school=school)
        serializer = ClubSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def club_detail(request, school, id):
    try:    
        clubs = Club.objects.filter(school=school)
        data = clubs.get(clubid=id)
    except Club.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        clubs = Club.objects.filter(school=school)
        data = clubs.get(clubid=id)
        serializer = ClubSerializer(data, context={'request': request}, many=False)

        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ClubSerializer(student, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)