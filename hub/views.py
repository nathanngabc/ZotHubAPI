from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import date, time
import numpy as np
import datetime



from .models import Club, Event, UserProfile, Tag
from .serializers import *

from rest_framework.permissions import IsAuthenticated

#Clubs

@api_view(['GET'])
def clubs_list(request, school):
    '''
    c = Club.objects.get(clubid="cyberuci")
    e1 = Event(name="Cyber Crime Prevention Workshop", description="A workshop for students to learn about cyber crime prevention and how to protect themselves online", club=c, starttime=time(9, 0), endtime=time(2, 0), date=date(2023, 3, 13), location="School Computer Lab", type="Cyber Crime Prevention Workshop", featured=True, memberCount=100)


    e1.save()
    tag1 = Tag.objects.get(name="Computer")
    tag2 = Tag.objects.get(name="STEM")
    e1.tags.add(tag1)
    e1.tags.add(tag2)
    '''

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
    return Response({'success': True})

@api_view(['GET'])
def popularevents(request, school):
    clubs = Club.objects.filter(school=school)
    clubs = Club.objects.all().order_by('memberCount').values()
    eventslist = []
    for e in Event.objects.all():
        if e.club in clubs:
            eventslist.append([e.memberCount, e])
    if n > len(eventslist): n = len(eventslist)
    eventslist = sorted(eventslist,key=lambda l:l[0], reverse=True)[0:n]  
    for e in eventslist:
        e[1].featured=True
    return EventSerializer(eventslist, context={'request': request}, many=True)

@api_view(['POST'])
def search(request, school):
    search_results = [["Events"], ["Clubs"], ["Tags"]]
    searchTerm = request.data.get("searchterm")
    for e in Event.objects.filter(school=school):
        if searchTerm in e.name or searchTerm in e.description:
            search_results[0].append(e.id)
        else:
            for t in e.tags.all():
                if e in t.name:
                    search_results[0].append(e.id)
    for c in Club.objects.filter(school=school):
        if searchTerm in c.name or searchTerm in c.description:
            search_results[1].append(c.clubid)
        else:
            for t in c.tags:
                if c in t.name:
                    search_results[1].append(c.clubid)
    for t in Tag.objects.all():
        if searchTerm in t.name:
            search_results[2].append(t.name)

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
    user = UserProfile.objects.get(username=Token.objects.get(token).user.username)
    return Response({'success': True, 'token': token.key})

@api_view(["GET"])
def recommendation(request, school):
    tags = ['Academic', 'Art', 'Athletics', 'Band', 'Book', 'Chess', 'Chorus', 'Community', 'Competition',
        'Computer', 'Dance', 'Debate', 'Drama', 'Educational', 'Engineering', 'Ensemble', 'Environmental',
        'Fitness', 'Foreign', 'Games', 'Gardening', 'History', 'Journalism', 'Language', 'Leadership', 'Literary',
        'Math', 'Music', 'Photography', 'Poetry', 'Politics', 'Science', 'Scouting', 'Service', 'Shakespeare', 'Social',
        'Speech', 'Sports', 'STEM', 'Student', 'Technology', 'Theater', 'Tourism', 'Tradition', 'Travel', 'Volunteering',
        'Wellness', 'Writing', 'Games', 'Magic', 'Food', 'Formal', 'Dinner', 'Lunch', 'Presentation']
    tagval = np.load('./hub/prebuiltModelTagsSimilarity.npy')
    things_user_in = []
    try:
        user = UserProfile.objects.get(username=Token.objects.get(key=request.GET.get("token", '')).user.username)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    userPreferences = set()
    for t in user.following_tags.all():
        userPreferences.add(t.name)
        things_user_in.append(t.name)
    for c in user.following_clubs.all():
        things_user_in.append(c.clubid)
        for t in c.tags.all():
            userPreferences.add(t.name)
    for e in user.following_events.all():
        things_user_in.append(e.id)
        for t in e.tags.all():
            userPreferences.add(t.name)
    userPreferences = list(userPreferences)
    up = []
    for t in userPreferences:
        if t in tags:
            up.append(tags.index(t))
    
    #clubs recommendation
    clubs_similar = []
    for c in Club.objects.all():
        c_vals = []
        for t in c.tags.all():
            if t.name in tags:
                c_vals.append(tags.index(t.name))
        val = 0
        for i in up:
            for j in c_vals:
                val+=float(tagval[i][j])
        if c.clubid not in things_user_in:
            clubs_similar.append([c.clubid, val])
    clubs_similar.sort(key=lambda x: x[1], reverse=True)
    clubs_similar = clubs_similar[0:3]
    #events recommendation
    events_similar = []
    for e in Event.objects.all():
        e_vals = []
        for t in e.tags.all():
            if t.name in tags:
                e_vals.append(tags.index(t.name))
        val = 0
        for i in up:
            for j in e_vals:
                val+=float(tagval[i][j])
        if e.id not in things_user_in:
            events_similar.append([e.id, val])
    events_similar.sort(key=lambda x: x[1], reverse=True)
    events_similar = events_similar[0:3]
    #tags recommendation
    tags_similar = []
    for e in Tag.objects.all():
        e_vals = []
        if t.name in tags:
            e_vals.append(tags.index(t.name))
        val = 0
        for i in up:
            for j in e_vals:
                val+=float(tagval[i][j])
        if e.name not in things_user_in:
            tags_similar.append([e.name, val])
    tags_similar.sort(key=lambda x: x[1], reverse=True)
    tags_similar = tags_similar[0:3]

    return Response({'success': True, 'clubs': clubs_similar, 'events': events_similar, 'tags': tags_similar})