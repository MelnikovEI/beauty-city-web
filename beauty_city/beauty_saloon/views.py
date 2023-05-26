import uuid


from django.shortcuts import render, redirect
from django.conf import settings
from beauty_saloon.models import Appointment, Client, Tip, Salon, Master, Service

from yookassa import Configuration, Payment


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
    context = {}
    #if request.method == 'POST':
        #appointment = Appointment.objects.create()
        #appointment_id = appointment.id
        #return redirect(f'/serviceFinally/{appointment_id}')
    return render(request, 'service.html', context)


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
        Tip.objects.update_or_create(
            amount=request.POST['value_tips'],
            client=appointment.client,
            master=appointment.master
        )

        payment = Payment.create({
            "amount": {
                "value": appointment.service.price + int(request.POST['value_tips']),
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
    appointments = client.appointment_set.all

    context = {
        'client': client,
        'appointments': appointments
    }
    return render(request, 'notes.html', context)


def admin(request):
    context = {}
    return render(request, 'admin.html', context)

