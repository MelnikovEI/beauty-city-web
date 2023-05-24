from django.contrib import admin
from .models import Salon, Master, Service, Client, Schedule, Appointment


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_info', 'description')



@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title',  'salon', 'employment_date')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('master', 'start_time', 'end_time')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'service', 'date_time')
