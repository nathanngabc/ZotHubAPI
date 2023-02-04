from django.db import models

class Club(models.Model):
    name = models.CharField("Name", max_length=100, primary_key=True)
    description = models.CharField("Description", max_length=600)
    email = models.EmailField()
    school = models.CharField("School", max_length = 100)
    clubid = models.CharField("clubid", max_length = 100)

    def __str__(self):
        return self.name

# Create your models here.
class Event(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.CharField("Description", max_length=600)
    club = models.ForeignKey(Club, on_delete = models.CASCADE, related_name="host")
    time = models.TimeField()
    location = models.CharField("Location", max_length = 100)

    def __str__(self):
        return self.name
