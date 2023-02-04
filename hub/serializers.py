from rest_framework import serializers
from .models import Club, Event

class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club 
        fields = ('name', 'description', 'email', 'school', 'clubid')

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('name', 'description', 'club', 'starttime', 'endtime', 'date', 'location', 'type', 'id')