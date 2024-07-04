from .models import *

def menu_links(request):
    links = Car.objects.all()
    return dict(links=links)