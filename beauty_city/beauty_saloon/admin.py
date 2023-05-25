from django.contrib import admin
from .models import Salon, Master, Service, Client, Schedule, Appointment, Review, PromoCode, Tip, ServiceCategory


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_info', 'description')



@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'title',  'salon', 'employment_date')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'comment', 'rating')


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'amount')
