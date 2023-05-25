from django.shortcuts import render

from .models import Salon, Master, Service, ServiceCategory


def index(request):
    salons = Salon.objects.all()
    masters = Master.objects.all()
    services = Service.objects.all()
    context = {
        "salons": salons,
        "masters": masters,
        "services": services
    }
    return render(request, 'index.html', context)


def service(request):
    salons = Salon.objects.all()
    masters = Master.objects.all()
    services = Service.objects.all()
    service_categories = ServiceCategory.objects.all()
    context = {
        "salons": salons,
        "masters": masters,
        "services": services,
        "service_categories": service_categories
    }
    return render(request, 'service.html', context)


def serviceFinally(request):
    context = {}
    return render(request, 'serviceFinally.html', context)


def popup(request):
    context = {}
    return render(request, 'popup.html', context)


def notes(request):
    context = {}
    return render(request, 'notes.html', context)


def admin(request):
    context = {}
    return render(request, 'admin.html', context)

