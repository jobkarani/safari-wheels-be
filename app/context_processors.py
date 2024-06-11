from .models import *

def menu_links(request):
    links = Brand.objects.all()
    return dict(links=links)