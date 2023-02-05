"""zothubapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from hub import views
from django.conf.urls import include
from rest_framework.authtoken import views as v
from rest_framework.authtoken.models import Token


urlpatterns = [
    path('admin/', admin.site.urls),  #admin
    path('api/<str:school>/clubs', views.clubs_list),   #get list of clubs based on school
    path('api/<str:school>/club/<str:id>', views.club_detail),   #get specific club info based on school + string club id
    path('api/<str:school>/events', views.events_list),   #get list of events per school
    path('api/<str:school>/event/<int:id>', views.event_detail), #gets individual detials on club
    path('api/profile', views.ProfileView), #get profile information, requires token auth; also post info
    path('api/createuser', views.ProfileCreate), #create profile, returns token auth
    path('api-token-auth', v.obtain_auth_token, name='api-token-auth'), #returns token auth, requires username/password
    path('api/<str:school>/club/<str:id>/events', views.club_events_list) #returns list of events per school, club
]
