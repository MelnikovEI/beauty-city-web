import uuid
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from beauty_saloon.models import Appointment, Client, Tip, Salon, Master, \
    Service, Review, Category, Schedule

from yookassa import Configuration, Payment


def index(request):
    salons = Salon.objects.all()
    masters = Master.objects.all()
    services = Service.objects.all()
    review = Review.objects.all()
    context = {
        "salons": salons,
        "masters": masters,
        "services": services,
        "reviews": review
    }
    return render(request, 'index.html', context)


def service(request):
    salons = Salon.objects.all()
    context = {
        "salons": salons,
    }

    return render(request, 'service.html', context)


def get_categories(request):
    categories = Category.objects.all()
    category_list = []

    for category in categories:
        category_data = {
            'id': category.id,
            'name': category.name,
            'services': []
        }

        services = Service.objects.filter(category=category)
        for service in services:
            service_data = {
                'id': service.id,
                'name': service.name,
                'price': float(service.price)
            }
            category_data['services'].append(service_data)

        category_list.append(category_data)

    return JsonResponse(category_list, safe=False)


def get_masters(request):
    salon_id = request.GET.get('salon_id')
    service_id = request.GET.get('service_id')

    masters = Master.objects.filter(salon_id=salon_id, services__id=service_id)
    master_list = []

    for master in masters:
        master_data = {
            'id': master.id,
            'first_name': master.first_name,
            'last_name': master.last_name,
            'speciality': master.speciality,
            'photo_url': master.photo.url if master.photo else None
        }

        master_list.append(master_data)

    return JsonResponse(master_list, safe=False)


def get_available_time(request):
    try:
        employee_work_day = Schedule.objects.get(
            master_id=int(request.GET.get('master_id')),
            day_of_week=request.GET.get('weekday')
        )
    except Schedule.DoesNotExist:
        return JsonResponse([], safe=False)
    if not employee_work_day.active:
        return JsonResponse([], safe=False)
    appointments = Appointment.objects.filter(
        master_id=request.GET.get('master_id'),
        date=request.GET.get('date')
    ).values_list('appointment_hour', flat=True)
    time_begins = set(map(lambda time: time.split(' - ')[0], appointments))
    free_times = list(Appointment.day_times.difference(time_begins))
    free_sorted_times = sorted(free_times, key=lambda time: datetime.strptime(time, '%H:%M'))
    return JsonResponse(free_sorted_times, safe=False)


def create_appointment(request):
    appointment = Appointment.objects.create(
        master_id=int(request.GET.get('master_id')),
        service_id=int(request.GET.get('service_id')),
        date=request.GET.get('date'),
        appointment_hour=request.GET.get('hour')
    )
    return JsonResponse(appointment.id, safe=False)


def serviceFinally(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    context = {'appointment': appointment}

    if request.method == 'POST':
        client = Client.objects.update_or_create(
            first_name=request.POST['fname'],
            phone_number=request.POST['tel']
        )
        appointment.client = client[0]
        appointment.save()
        return redirect(f'/popup/{appointment_id}')
    return render(request, 'serviceFinally.html', context)


def payment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_API_KEY
    allowed_host = settings.ALLOWED_HOSTS
    port = settings.PORT

    payment = Payment.find_one(appointment.payment_id)
    if payment.paid:
        appointment.is_paid = True
        appointment.save()
        client_id = appointment.client.id
        return redirect(f"http://{allowed_host[0]}:{port}/notes/{client_id}")
    return render(request, 'paid-not-success.html')


def popup(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    context = {'appointment': appointment}
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_API_KEY
    allowed_host = settings.ALLOWED_HOSTS[0]
    port = settings.PORT

    if request.method == 'POST':
        tips = request.POST['value_tips']
        if not tips:
            tips = 0
        Tip.objects.update_or_create(
            amount=tips,
            client=appointment.client,
            master=appointment.master
        )

        payment = Payment.create({
            "amount": {
                "value": appointment.service.price + int(tips),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f"http://{allowed_host}:{port}/payment/{appointment_id}/"
            },
            "capture": True,
            "description": f"Услуга №{appointment.id} - {appointment.service.name}"
                           f"Цена - {appointment.service.price}"
        }, uuid.uuid4())

        appointment.payment_id = payment.id
        appointment.save()
        redirect_url = payment.confirmation.confirmation_url
        return redirect(redirect_url)
    return render(request, 'popup.html', context)


def notes(request, client_id):
    client = Client.objects.get(id=client_id)
    appointments = client.appointment_set.all()
    future_appointment = []
    last_appointment = []
    x = datetime.now()

    for appointment in appointments:
        if appointment.date_time.day <= datetime.now().day:
            future_appointment.append(appointment)
        else:
            last_appointment.append(appointment)

    context = {
        'client': client,
        'future_appointment': future_appointment,
        'last_appointment': last_appointment,
    }
    return render(request, 'notes.html', context)


def admin(request):
    context = {}
    return render(request, 'admin.html', context)

