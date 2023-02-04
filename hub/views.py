from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models.query import QuerySet

from .models import Club
from .serializers import *

@api_view(['GET'])
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

@api_view(['GET'])
def club_detail(request, school, id):
    try:    
        clubs = Club.objects.filter(school=school)
        club = clubs.get(clubid=id)
    except Club.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ClubSerializer(club, context={'request': request}, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = ClubSerializer(club, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def events_list(request, school):
    if request.method == 'GET':
        clubs = Club.objects.filter(school=school)
        print(clubs)
        eventslist = []
        for e in Event.objects.all():
            if e.club in clubs:
                eventslist.append(e)
        serializer = EventSerializer(eventslist, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def event_detail(request, school, id):
    try:    
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EventSerializer(event, context={'request': request}, many=False)
        return Response(serializer.data)

