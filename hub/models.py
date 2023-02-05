from django.db import models
from django.contrib.auth.models import User



class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=600)
    email = models.EmailField()
    school = models.CharField("School", max_length = 100)
    clubid = models.CharField("clubid", max_length = 100, primary_key=True)
    imageURL = models.CharField(max_length = 300)
    memberCount = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name="club_tags")

    def __str__(self):
        return self.clubid

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    club = models.ForeignKey(Club, on_delete = models.CASCADE, related_name="host")
    starttime = models.TimeField()
    endtime = models.TimeField()
    date = models.DateField()
    featured = models.BooleanField(default=False)
    location = models.CharField(max_length = 100)
    type = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True, related_name="event_tags")
    memberCount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    username = models.CharField(max_length=40, unique=True)
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)

    following_tags = models.ManyToManyField(Tag, blank=True, related_name="user_tags")
    following_clubs = models.ManyToManyField(Club, blank=True, related_name="user_clubs")
    following_events = models.ManyToManyField(Event, blank=True, related_name="user_events")

    clubs_owned = models.ManyToManyField(Club, blank=True, related_name = "owned_clubs")
    
    school = models.CharField(max_length=100, default="uci")

    def __str__(self):
        return self.username
