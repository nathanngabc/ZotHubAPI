from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime


from .models import Club, Event, UserProfile, Tag
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

@api_view(['POST'])
def club_create(request, school):
    try:
        user = UserProfile.objects.get(username=Token.objects.get(key=request.GET.get("token", '')).user.username)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    d = request.data
    c = Club(name=d.get("name"), description=d.get("description"), email=d.get("email"), school=school, clubid=d.get("clubid"), 
    imageURL=d.get("imageurl"), memberCount=0)
    for t in d.get("tags").split("|"):
        tag = Tag.objects.get(name=t)
        c.tags.add(tag)
    c.save()
    user.clubs_owned.add(c)
    return Response({'success': True})
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
    return Response({'success': True})

@api_view(['POST'])
def event_create(request, school):
    d = request.data
    c = Event(name=d.get("name"), description=d.get("description"), s=datetime.strptime(d.get("starttime"), '%H::%M::%S').time(),
        endtime=datetime.strptime(d.get("endtime"), '%H::%M::%S').time(), date=datetime.strptime(d.get("date"), '%m-%d-%Y').date(),
        featured=False, location=d.get("location"), type=d.get("type"), memberCount=0)
    c.club.add(Club.objects.get(clubid=d.get("club")))
    for t in d.get("tags").split("|"):
        tag = Tag.objects.get(name=t)
        c.tags.add(tag)
    c.save()
#USERS

@api_view(['GET', 'POST'])
def ProfileView(request):
    try:
        user = UserProfile.objects.get(username=Token.objects.get(key=request.GET.get("token", '')).user.username)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        data = userSerializers(user, context={'request': request}, many=False)
        return Response(data.data)
    if request.method == 'POST':
        typeAdded = request.data.get("type")
        action = request.data.get("action")
        if typeAdded == "tag":
            tag_added = request.data.get("tag")
            tag = Tag.objects.get(name=tag_added)
            if action == "add": user.following_tags.add(tag)
            elif action == "remove": user.following_tags.remove(tag)
        elif typeAdded == "club":
            club_added = request.data.get("club")
            club = Club.objects.get(clubid=club_added)
            if action == "add":
                user.following_clubs.add(club)
                club.memberCount += 1
            elif action == "remove":
                user.following_clubs.remove(club)
                club.memberCount += -1
        elif typeAdded == "event":
            event_added = request.data.get("event")
            event = Event.objects.get(id=event_added)
            if action == "add":
                user.following_events.add(event)
                event.memberCount += 1
            elif action == "remove":
                user.following_events.remove(event)
                event.memberCount += -1

        return Response({'success': True})

@api_view(['POST'])
def ProfileCreate(request):
    user = User.objects.create_user(username=request.data.get("username"),
                                 email=request.data.get("email"),
                                 password=request.data.get("password"))
    user.save()
    userprofile = UserProfile(username = request.data.get("username"), associated_user = user, school=request.data.get("school"))
    userprofile.save()
    token = Token.objects.create(user=user)
    return Response({'success': True, 'token': token.key})