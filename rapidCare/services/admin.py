from django.contrib import admin
from services.models import (
    Coupon,
    Checkout,
    Cart,
    Pricing,
    Worker,
    Days,
    Service,
    ServiceGarden,
    ServiceCarWash,
    ServiceHouseKeeping,
    Booking,
    CarData,
)


class CouponAdminConfig(admin.ModelAdmin):
    list_display = ('name', 'serviceType', 'onetime', 'subscription',
                    'percentageDiscount', 'discount', 'uses')


class CheckoutAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'user', 'datetime', 'address')


class PricingAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('name', 'price',)


class WorkerAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('serviceType', 'numOfWorkers',)


class DaysAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('service', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat')


class BookingAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('service', 'date',)


class ServiceAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id','checkoutRef', 'serviceType', 'package',
                    'price', 'startDate', 'endDate',)


class ServiceHouseKeepingAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('hours', 'maids', 'supplies',)


class CarDataAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('make', 'carModel', 'price')


# Register your models here.
admin.site.register(Coupon, CouponAdminConfig)
admin.site.register(Checkout, CheckoutAdminConfig)
# admin.site.register(ServiceGarden, ServiceGardenAdminConfig)
# admin.site.register(ServiceCarWash, ServiceCarWashAdminConfig)
admin.site.register(Days, DaysAdminConfig)
admin.site.register(Service, ServiceAdminConfig)
admin.site.register(ServiceGarden)
admin.site.register(ServiceCarWash)
admin.site.register(Cart)
admin.site.register(Pricing, PricingAdminConfig)
admin.site.register(Worker, WorkerAdminConfig)
admin.site.register(ServiceHouseKeeping, ServiceHouseKeepingAdminConfig)
admin.site.register(Booking, BookingAdminConfig)
admin.site.register(CarData, CarDataAdminConfig)
