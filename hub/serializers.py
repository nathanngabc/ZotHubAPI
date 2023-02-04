from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Club, Event, UserProfile
from django.contrib.auth.models import User


class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club 
        fields = ('name', 'description', 'email', 'school', 'clubid')

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('name', 'description', 'club', 'starttime', 'endtime', 'date', 'location', 'type', 'id')

class userSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = UserProfile
        fields =  ('username', 'following_tags', 'following_clubs', 'following_events')