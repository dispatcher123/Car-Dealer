from .models import CarModel,Message


def cars_links(request):
    links=CarModel.objects.all()
    return dict(links=links)

def CountNotifications(request):
    count_notifications= 0
    
    if request.user.is_authenticated:
        count_notifications= Message.objects.filter(user=request.user,is_read=False).count()
    return {'count_notifications' : count_notifications}

##### USER PAGE



