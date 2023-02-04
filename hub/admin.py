from django.contrib import admin

# Register your models here.
from .models import Club, Event

# Register your models here.
admin.site.register(Club)
admin.site.register(Event)