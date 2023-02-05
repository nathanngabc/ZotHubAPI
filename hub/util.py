from .models import Club, Event, UserProfile, Tag

def selectPopular(school, n=4):
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


    


if __name__ == "__main__":
    pass