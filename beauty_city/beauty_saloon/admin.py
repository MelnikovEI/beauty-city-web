from django.contrib import admin
from .models import Salon, Master, Service, Client, Schedule, Appointment


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_info', 'description', 'photo')  
    list_filter = ('name', 'address', 'contact_info', 'description', 'photo')
    search_fields = ('name', 'address', 'contact_info', 'description', 'photo')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'speciality', 'salon', 'photo', 'employment_date')
    list_filter = ('first_name', 'last_name', 'speciality', 'salon', 'photo', 'employment_date')
    search_fields = ('first_name', 'last_name', 'speciality', 'salon', 'photo', 'employment_date')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'photo', 'duration')
    list_filter = ('name', 'price', 'photo', 'duration')
    search_fields = ('name', 'price', 'photo', 'duration')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('first_name', 'last_name', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('master', 'start_time', 'end_time')
    list_filter = ('master', 'start_time', 'end_time')
    search_fields = ('master', 'start_time', 'end_time')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'service', 'date_time')
    list_filter = ('client', 'master', 'service', 'date_time')
    search_fields = ('client', 'master', 'service', 'date_time')
