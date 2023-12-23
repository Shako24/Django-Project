from django.db import models
from datetime import datetime
from userAuth.models import CustomUser
from shortuuid.django_fields import ShortUUIDField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

couponTypes = (
    ('all', 'all'),
    ('grdn', 'grdn'),
    ('cwsh', 'cwsh'),
    ('hskp', 'hskp'),
    ('vhmn', 'vhmn'),
    ('vppi', 'vppi'),
)


class Coupon(models.Model):
    # id = ShortUUIDField(primary_key=True, length=5,
    #                     max_length=5, editable=False)
    name = models.CharField(primary_key=True, max_length=25)
    # couponType = models.CharField(
    #     max_length=4, choices=couponTypes, default='all')
    serviceType = models.CharField(
        max_length=4, choices=couponTypes, default='all')
    onetime = models.BooleanField(default=False)
    subscription = models.BooleanField(default=False)
    percentageDiscount = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=7, decimal_places=2)
    maxDiscount = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=50, null=True, blank=True)
    uses = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.name}'


class Checkout(models.Model):
    id = ShortUUIDField(primary_key=True, length=11,
                        max_length=11, editable=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    phone = PhoneNumberField()
    datetime = models.DateTimeField(default=datetime.now, blank=True)
    address = models.TextField(default='None')
    servicesPrice = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    discount = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    vat = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    extraCost = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    total = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    cashOnDelivery = models.BooleanField(default=False)
    payed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'


class Cart(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    deviceID = models.CharField(
        max_length=36, null=True, blank=True, unique=True)
    dateCreated = models.DateField(default=datetime.now)

    def __str__(self):
        return f'{self.user}({self.deviceID})\'s cart'


class Pricing(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price}'


class Worker(models.Model):
    serviceType = models.CharField(max_length=4)
    numOfWorkers = models.IntegerField()

    def __str__(self):
        return f'{self.serviceType} - {self.numOfWorkers}'


packageChoices = (
    ('one-time', 'one-time'),
    ('subscription', 'subscription')
)


class Service(models.Model):
    serviceType = models.CharField(max_length=30)
    package = models.CharField(
        max_length=25, choices=packageChoices, default='one-time')
    startDate = models.DateField(default=datetime.now, blank=True)
    endDate = models.DateField(default=datetime.now, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    numOfDays = models.IntegerField(default=1)
    # workersAssigned = models.ForeignKey(
    #     Worker, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    cartRef = models.ForeignKey(
        Cart, on_delete=models.SET_NULL, null=True, blank=True)
    checkoutRef = models.ForeignKey(
        Checkout, on_delete=models.SET_NULL, null=True, blank=True)
    paused = models.BooleanField(default=False)
    autoRenew = models.BooleanField(default=True)
    description = models.TextField(default='None')


    def __str__(self):
        return f'id: {self.id} - {self.serviceType}: {self.package}'


class ServiceGarden(models.Model):
    general = models.OneToOneField(
        Service, on_delete=models.CASCADE, null=True)
    packageName = models.TextField(default='None')

    def __str__(self):
        return f'grdn: {self.general.package}'


class ServiceCarWash(models.Model):
    general = models.OneToOneField(
        Service, on_delete=models.CASCADE, null=True)
    basicExteriorWash = models.IntegerField(default=0, blank=True, null=True)
    interiorCleaning = models.IntegerField(default=0, blank=True, null=True)
    BasicExteriorWithinteriorCleaning = models.IntegerField(
        default=0, blank=True, null=True)
    exteriorWashWithWax = models.IntegerField(default=0, blank=True, null=True)
    superDirtyExteriorWash = models.IntegerField(
        default=0, blank=True, null=True)
    engineDetailing = models.IntegerField(default=0, blank=True, null=True)
    basicExteriorWashSUV = models.IntegerField(
        default=0, blank=True, null=True)
    interiorCleaningSUV = models.IntegerField(default=0, blank=True, null=True)
    BasicExteriorWithinteriorCleaningSUV = models.IntegerField(
        default=0, blank=True, null=True)
    exteriorWashWithWaxSUV = models.IntegerField(
        default=0, blank=True, null=True)
    superDirtyExteriorWashSUV = models.IntegerField(
        default=0, blank=True, null=True)
    engineDetailingSUV = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f'cwsh: {self.general.package}'


class ServiceHouseKeeping(models.Model):
    general = models.OneToOneField(
        Service, on_delete=models.CASCADE, null=True)
    hours = models.FloatField()
    maids = models.IntegerField()
    supplies = models.BooleanField(default=False)

    def __str__(self):
        return f'hskp: {self.general.package}'


class Days(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    sun = models.BooleanField(default=False)
    mon = models.BooleanField(default=False)
    tue = models.BooleanField(default=False)
    wed = models.BooleanField(default=False)
    thu = models.BooleanField(default=False)
    fri = models.BooleanField(default=False)
    sat = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.service.serviceType}: {self.service.package}'


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'service ID: {self.service.id} | time/date: {self.time}/{self.date}'


class CarData(models.Model):
    make = models.CharField(max_length=25)
    carModel = models.CharField(max_length=25)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.make} {self.carModel}: {self.price}'
