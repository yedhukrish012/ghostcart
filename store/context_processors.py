from .models import category


def menulinks(request):
    links = category.objects.all()
    return dict(links = links)