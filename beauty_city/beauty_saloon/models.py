import datetime
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Salon(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='salon_photos', blank=True)

    def __str__(self):
        return self.name


class Master(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, )
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100, null=True)
    services = models.ManyToManyField('Service')
    photo = models.ImageField(upload_to='master_photos', blank=True)
    employment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_experience(self):
        if not self.employment_date:
            return 'Нет опыта'
        experience = datetime.date.today() - self.employment_date
        years = experience.days//365
        years_txt = str(years)
        months = (experience.days % 365) // 30
        if years == 0:
            return f'{months} мес.'
        if years_txt[-1] in ('1', '2', '3', '4'):
            years_txt = str(years_txt) + ' г.'
        else:
            years_txt = str(years_txt) + ' л.'
        return f'{years_txt} {months} мес.'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='service_photos', blank=True)
    duration = models.DurationField(default='00:30:00')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = PhoneNumberField()
    email = models.EmailField(blank=True, null=True)
    photo = models.ImageField(upload_to='client_photos', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number}"


class Schedule(models.Model):
    MONDAY = 'Mo'
    TUESDAY = 'Tu'
    WEDNESDAY = 'We'
    THURSDAY = 'Td'
    FRIDAY = 'Fr'
    SATURDAY = 'Sa'
    SUNDAY = 'Su'

    DAYS_OF_WEEK = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday')
    ]

    day_of_week = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK,
        blank=True
    )

    active = models.BooleanField(
        default=False
    )
    master = models.ForeignKey(Master, on_delete=models.CASCADE)

    def __str__(self):
        return f"Schedule for {self.master} on {self.day_of_week}"


class Appointment(models.Model):
    MORNING_1 = '9:00'
    MORNING_2 = '10:00'
    MORNING_3 = '11:00'
    AFTERNOON_1 = '12:00'
    AFTERNOON_2 = '13:00'
    AFTERNOON_3 = '14:00'
    DAY_1 = '15:00'
    DAY_2 = '16:00'
    DAY_3 = '17:00'
    EVENING_1 = '18:00'
    EVENING_2 = '19:00'
    EVENING_3 = '20:00'
    day_times = {
        MORNING_1, MORNING_2, MORNING_2, MORNING_3, AFTERNOON_1, AFTERNOON_2,
        AFTERNOON_3, DAY_1, DAY_2, DAY_3, EVENING_1, EVENING_2, EVENING_3
    }
    WORK_HOURS = [
        (MORNING_1, MORNING_1),
        (MORNING_2, MORNING_2),
        (MORNING_3, MORNING_3),
        (AFTERNOON_1, AFTERNOON_1),
        (AFTERNOON_2, AFTERNOON_2),
        (AFTERNOON_3, AFTERNOON_3),
        (DAY_1, DAY_1),
        (DAY_2, DAY_2),
        (DAY_3, DAY_3),
        (EVENING_1, EVENING_1),
        (EVENING_2, EVENING_2),
        (EVENING_3, EVENING_3),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_hour = models.CharField(
        max_length=15,
        choices=WORK_HOURS,
        blank=True
    )
    date = models.DateField(null=True, blank=True)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
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


class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.client} for {self.master}"
