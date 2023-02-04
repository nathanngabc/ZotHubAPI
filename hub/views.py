from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


from .models import Club, Event, UserProfile
from .serializers import *

from rest_framework.permissions import IsAuthenticated

#Clubs

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
def club_events_list(request, school, id):
    try:    
        clubs = Club.objects.filter(school=school)
        club = clubs.get(clubid=id)
    except Club.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    eventslist = []
    for e in Event.objects.all():
        if e.club == club:
            eventslist.append(e)
    serializer = EventSerializer(eventslist, context={'request': request}, many=True)
    return Response(serializer.data)    

#Events

@api_view(['GET'])
def events_list(request, school):
    if request.method == 'GET':
        clubs = Club.objects.filter(school=school)
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

#USERS

@api_view(['GET'])
def ProfileView(request):
    user = UserProfile.objects.get(username=Token.objects.get(key=request.GET.get("token", '')).user.username)
    
    if request.method == 'GET':
        print(user)
        data = userSerializers(user, context={'request': request}, many=False)
        return Response(data.data)

@api_view(['POST'])
def ProfileCreate(request):
    print(request.data)
    user = User.objects.create_user(username=request.data.get("username"),
                                 email=request.data.get("email"),
                                 password=request.data.get("password"))
    user.save()
    userprofile = UserProfile(username = request.data.get("username"), associated_user = user)
    userprofile.save()
    token = Token.objects.create(user=user)
    return Response({'success': True, 'token': token.key})