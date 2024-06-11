from .models import *

def menu_links(request):
    links = Model.objects.all()
    return dict(links=links)