from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Salon(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='salon_photos', blank=True)

    def __str__(self):
        return self.name


class Master(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    speciality = models.TextField()
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    services = models.ManyToManyField('Service')
    photo = models.ImageField(upload_to='master_photos', blank=True)
    employment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='service_photos', blank=True)
    duration = models.DurationField(default='00:30:00')

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Schedule(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Schedule for {self.master}"


class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment of {self.client} with {self.master}"


class Tip(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tip of {self.amount} by {self.client}"


class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.code
