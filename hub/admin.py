from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
from .models import Club, Event, UserProfile, Tag

# Register your models here.
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(UserProfile)
admin.site.register(Tag)