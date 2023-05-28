"""beauty_city URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from beauty_saloon import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('service/', views.service, name='service'),
    path('service/get_categories', views.get_categories, name='get_categories'),
    path('service/get_masters', views.get_masters, name='get_masters'),
    path('service/get_available_time', views.get_available_time, name='get_available_time'),
    path('service/create_appointment', views.create_appointment, name='create_appointment'),
    path('serviceFinally/<int:appointment_id>/', views.serviceFinally, name='serviceFinally'),
    path('popup/<int:appointment_id>/', views.popup, name='popup'),
    path('payment/<int:appointment_id>/', views.payment, name='payment'),
    path('notes/<int:client_id>/', views.notes, name='notes'),
    path('admin/', views.admin, name='admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
