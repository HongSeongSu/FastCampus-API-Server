from django.http import HttpResponse


def index(request):
    return HttpResponse('FastCampus API Server')
