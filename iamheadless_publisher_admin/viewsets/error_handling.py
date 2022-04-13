from django.shortcuts import render
from django.template import RequestContext

from ..conf import settings


def handler403(request, *args, **argv):
    return render(request, f'{settings.APP_NAME}/403.html', context={}, status_code=403)


def handler404(request, *args, **argv):
    return render(request, f'{settings.APP_NAME}/403.html', context={}, status_code=404)


def handler500(request, *args, **argv):
    return render(request, f'{settings.APP_NAME}/403.html', context={}, status_code=500)
