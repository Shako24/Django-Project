from django.shortcuts import render, redirect
from django.contrib import messages
from services.models import (
    Days,
    Service,
    ServiceGarden,
    ServiceCarWash,
    ServiceHouseKeeping,
    Booking,
    Cart,
    Pricing,
    Coupon,
    Checkout,
    Worker,
    CarData,
)
from userAuth.models import Address
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from userAuth.models import Address
from datetime import datetime, timedelta, date
import pandas as pd
from decimal import *
import calendar
from copy import deepcopy
# For emails
from django.core.mail import EmailMultiAlternatives
from rapidCare.settings import EMAIL_HOST_USER
from userAuth.email_helper import img_data, emailInvoice
# For payment gateway
import requests
import json
import webbrowser

# Create your views here.


def checkoutView(request):
    addresses = None
    cart = None
    discount = 0
    servicesPrice = 0
    coupon = None
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        addresses = Address.objects.filter(user=request.user)
    else:
        device = request.COOKIES['device']
        cart = Cart.objects.get(deviceID=device)
        addresses = Address.objects.filter(deviceID=device)

    services = Service.objects.filter(cartRef=cart)
    if len(services) == 0:
        messages.error(request, 'No items in cart')
        return redirect('cart')

    for service in services:
        servicesPrice += service.price
    serviceVat = float(servicesPrice) * 0.05
    totalPrice = float(servicesPrice) + serviceVat

    context = {
        'addresses': addresses,
        'services': services,
        'servicesPrice': servicesPrice,
        'vat': serviceVat,
        'discount': discount,
        'coupon': coupon,
        'totalPrice': totalPrice,
        'paymentPortal': False
    }

    if request.method == 'POST':
        coupon = None
        # getting the coupon
        if 'couponInput' in request.POST:
            couponID = request.POST['couponInput']

            # checking coupon name
            if couponID != '':
                try:
                    coupon = Coupon.objects.get(name=couponID)
                except:
                    messages.error(request, 'ERROR - incorrect coupon name')
                    return redirect('checkout')
                # checking how many times this user has used this coupon
                previousCheckouts = Checkout.objects.filter(coupon=coupon)
                if len(previousCheckouts) >= coupon.uses:
                    messages.error(
                        request, 'ERROR - The coupon\'s uses have run out')
                    return redirect('checkout')
                # Getting the discount that will be applied to services
                couponServicePrice = 0
                if coupon.percentageDiscount:
                    # getting the discount by percentage
                    if coupon.serviceType == 'all':
                        if coupon.onetime and coupon.subscription:
                            couponServicePrice = (float(coupon.discount)
                                                  * servicesPrice) / 100
                        elif coupon.onetime and not coupon.subscription:
                            for service in services:
                                if service.package == 'one-time':
                                    couponServicePrice += service.price
                        elif not coupon.onetime and coupon.subscription:
                            for service in services:
                                if service.package == 'subscription':
                                    couponServicePrice += service.price
                        discount = (float(coupon.discount) *
                                    float(couponServicePrice)) / 100
                    else:
                        for service in services:
                            if service.serviceType == coupon.serviceType:
                                if coupon.onetime and coupon.subscription:
                                    couponServicePrice += service.price
                                elif coupon.onetime and not coupon.subscription:
                                    if service.package == 'one-time':
                                        couponServicePrice += service.price
                                elif not coupon.onetime and coupon.subscription:
                                    if service.package == 'subscription':
                                        couponServicePrice += service.price
                        discount = (float(coupon.discount) *
                                    float(couponServicePrice)) / 100
                    # checking if applying the discount exceeds max discount for the coupon
                    if discount > float(coupon.maxDiscount):
                        discount = float(coupon.maxDiscount)
                else:
                    # getting the discount by cash
                    discount = float(coupon.discount)
                if (totalPrice - discount) < 20:
                    messages.error(
                        request, "ERROR - can't apply coupon for this total")
                    return redirect('checkout')
                newServicesPrice = 0
                # applying the discount
                if coupon.serviceType == 'all':
                    # applying to all services
                    newServicesPrice = servicesPrice - discount
                else:
                    # applying to specific service
                    difference = float(couponServicePrice) - discount
                    newServicesPrice = float(
                        servicesPrice) - float(couponServicePrice) + difference
                serviceVat = newServicesPrice * 0.05
                totalPrice = float(newServicesPrice) + serviceVat
                context['discount'] = discount
                context['vat'] = serviceVat
                context['totalPrice'] = totalPrice
                context['coupon'] = coupon.name
                context['paymentPortal'] = 'True'

                selectedAddress = request.POST['addressInput']
                print('The address selected is ', selectedAddress)
                for address in addresses:
                    if str(address) == selectedAddress:
                        context.update({'addressSelected': address})

                if 'paySubmit' not in request.POST:
                    return render(request, 'services/checkout.html', context)
        # completing the payment
        if 'paySubmit' in request.POST:
            # getting the address
            selectedAddress = request.POST.get('addressInput')
            if selectedAddress == None:
                messages.error(request, f'ERROR - Please select an address')
                return redirect('checkout')

            # setting the address to string
            addressFinal = None
            for address in addresses:
                if str(address) == selectedAddress:
                    addressFinal = f'Unit No.: {address.unitNo},\nArea: {address.area},\nBuilding Name: {address.buildingName},\nNearest Landmark: {address.nearestLandmark},\nState: {address.state}, \nGoogle Maps: {address.googleMapsLink}'

            email = None
            phone = None
            # deleting address of guest user
            if not request.user.is_authenticated:
                email = request.POST.get('guestEmailInput')
                phone = request.POST.get('guestPhoneInput')
                if email == '' or phone == '':
                    messages.error(
                        request, f'ERROR - Please enter your email and phone number')
                    return redirect('checkout')
                for address in addresses:
                    address.delete()
            else:
                if request.user.email == None or request.user.email == "":
                    email = request.POST.get('emailInput')
                else:
                    email = request.user.email
                
                if request.user.phone_number == None or request.user.phone_number == "":
                    phone = request.POST.get('phone_numberInput')
                else:
                    phone = request.user.phone_number

            if phone == None or phone == "":
                messages.error(request, 'Enter the phone number')
                return redirect('checkout')

            if email == None or email == "":
                messages.error(request, 'Enter the valid email address')
                return redirect('checkout')

            cashOnDelivery = False
            paymentType = request.POST.get('payment-method')
            if paymentType == 'card':
                cashOnDelivery = False
            elif paymentType == 'cash':
                cashOnDelivery = True

            # creating the Checkout object
            checkout = Checkout.objects.create(
                email=email,
                phone=phone,
                address=addressFinal,
                servicesPrice=servicesPrice,
                discount=context["discount"],
                vat=context["vat"],
                total=context["totalPrice"],
                coupon=coupon,
                cashOnDelivery=bool(cashOnDelivery),
            )

            # Setting the user value if user is authenticated
            if request.user.is_authenticated:
                checkout.user = request.user
                checkout.save()

            url = "https://business.mamopay.com/manage_api/v1/links"
            if not checkout.cashOnDelivery:
                payload = {
                    "custom_data": {
                        "val1": True,
                        "val2": "custom value"
                    },
                    "name": f"{checkout.id}",
                    "description": "basic exterior wash",
                    "capacity": 1,
                    "active": True,
                    "return_url": f"http://127.0.0.1/services/checkoutPayment/{checkout.id}",
                    "amount": checkout.total,
                    "enable_message": False,
                    "enable_tips": True,
                    "enable_customer_details": True
                }
                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "Authorization": "Token sk-c829bb50-69c5-4a1c-9f65-00f091b6a4a0"
                }
                response = requests.post(url, json=payload, headers=headers)
                jsonResponse = json.loads(response.text)  # string to json
                # back = json.dumps(jsonResponse)  # json to string
                webbrowser.open(jsonResponse['payment_url'], new=0)
                return redirect('index')
            else:
                return redirect('checkoutPayment', checkout)
    return render(request, 'services/checkout.html', context)


def servicesView(request):
    return render(request, 'services/services.html')


def vehicleInsuranceView(request):
    return render(request, 'services/vehicle_insurance.html')


@login_required
def gardenView(request):

    context = {
        'litePrice': Pricing.objects.get(name='garden-lite').price,
        'litePlusPrice': Pricing.objects.get(name='garden-lite-plus').price,
        'premiumPrice': Pricing.objects.get(name='garden-premium').price,
    }

    if request.method == 'POST':
        pricing = None
        days = 0
        if 'liteSubmit' in request.POST:
            pricing = Pricing.objects.get(name='garden-lite')
            packageName = 'Lite'
            days = 1
        if 'litePlusSubmit' in request.POST:
            pricing = Pricing.objects.get(name='garden-lite-plus')
            packageName = 'Lite Plus'
            days = 3
        if 'premiumSubmit' in request.POST:
            pricing = Pricing.objects.get(name='garden-premium')
            packageName = 'Premium'
            days = 4
        newGarden = Service.objects.create(
            serviceType='grdn',
            package='subscription',
            numOfDays=days,
            price=pricing.price,
            description=f"Package = {packageName}\n",
        )
        ServiceGarden.objects.create(
            general=newGarden,
            packageName=packageName,
        )
        # messages.success(request, f'{packageName} added to cart')
        return redirect('booking', newGarden.id)
    return render(request, 'services/garden.html', context)


def carWashView(request):

    if request.method == 'POST':
        try:
            option = request.POST['car-wash-option']

            if option == 'one-time':
                return redirect('singleCarWash')
            elif option == 'package':
                return redirect('packageCarWash')
            else:
                messages.error(request, 'Select Car Wash Option')
                return redirect('carWash')
        except:
            messages.error(request, 'Select Car Wash Option')
            return redirect('carWash')

    return render(request, 'services/car_wash.html')


def houseKeepingView(request):

    if request.method == 'POST':
        try:
            option = request.POST['house-keeping-option']

            if option == 'one-time':
                return redirect('houseKeepingSingle')
            elif option == 'package':
                return redirect('houseKeepingPackage')
            else:
                messages.error(request, 'Select House Keeping Option')
                return redirect('houseKeeping')
        except:
            messages.error(request, 'Select House Keeping Option')
            return redirect('houseKeeping')

    return render(request, 'services/house_keeping.html')


def vehicleCareView(request):

    if request.method == 'POST':
        try:
            option = request.POST['car-service-option']

            if option == 'vehicle-maintenance':
                return redirect('vehiclemaintenance')
            elif option == 'pre-purchase-inspection':
                return redirect('prepurchaseinspection')
            else:
                messages.error(request, 'Select Car Service Option')
                return redirect('carWash')
        except:
            messages.error(request, 'Select Car Service Option')
            return redirect('vehiclecare')

    return render(request, 'services/vehicleCare.html')


def houseKeepingSingleView(request):
    servicePrice = 0
    description = ''

    if request.method == 'POST':
        hoursInput = int(request.POST['hours'])
        maidsInput = int(request.POST['maids'])
        suppliesInput = False
        if (request.POST.get('supplies')) == 'true':
            suppliesInput = True
        elif (request.POST.get('supplies')) == 'false':
            suppliesInput = False

        servicePrice = hoursInput * maidsInput
        
        print('supplies is: ', suppliesInput)

        if suppliesInput == True:
            servicePrice *= Pricing.objects.get(name='hskp:withSupplies').price
        else:
            servicePrice *= Pricing.objects.get(
                name='hskp:withoutSupplies').price

        if suppliesInput:
            description = f'Hours: {hoursInput}\nMaids: {maidsInput}\nSupplies Required: Yes\n'
        else:
            description = f'Hours: {hoursInput}\nMaids: {maidsInput}\nSupplies Required: No\n'    

        newhskp = Service.objects.create(
            serviceType='hskp',
            package='one-time',
            price=servicePrice,
            description=description,
            autoRenew=False,
        )
        ServiceHouseKeeping.objects.create(
            general=newhskp,
            hours=hoursInput,
            maids=maidsInput,
            supplies=suppliesInput
        )
        return redirect('booking', newhskp.id)
    return render(request, 'services/houseService-single.html')


@login_required
def houseKeepingPackageView(request):
    servicePrice = 0
    if request.method == 'POST':
        try:
            hoursInput = float(request.POST['hours'])
            maidsInput = int(request.POST['maids'])
            suppliesInput = False
            if (request.POST.get('supplies')) == 'true':
                suppliesInput = True
            elif (request.POST.get('supplies')) == 'false':
                suppliesInput = False
            daysPerWeek = int(request.POST['days'])
        except:
            messages.error(request, 'Select all the required options')

        servicePrice = Decimal(hoursInput) * maidsInput * daysPerWeek * 4
        if suppliesInput == True:
            servicePrice *= Pricing.objects.get(name='hskp:withSupplies').price
        else:
            servicePrice *= Pricing.objects.get(
                name='hskp:withoutSupplies').price

        

        if daysPerWeek*hoursInput*maidsInput >= 12:
            servicePrice *= Decimal(0.9)

        description = f'Hours: {hoursInput}\nMaids: {maidsInput}\nSupplies Required: {suppliesInput}\nDays Per Week: {daysPerWeek}\n'

        newhskp = Service.objects.create(
            serviceType='hskp',
            package='subscription',
            numOfDays=daysPerWeek,
            price=servicePrice,
            description=description,
        )
        ServiceHouseKeeping.objects.create(
            general=newhskp,
            hours=hoursInput,
            maids=maidsInput,
            supplies=suppliesInput
        )
        return redirect('booking', newhskp.id)
    return render(request, 'services/houseService-package.html')


def singleCarWashView(request):
    price = 0
    description = ''
    context = {
        'basicExteriorWashPrice': Pricing.objects.get(name='basicExteriorWash').price,
        'basicExteriorWashSUVPrice': Pricing.objects.get(name='basicExteriorWashSUV').price,
        'interiorCleaningPrice': Pricing.objects.get(name='interiorCleaning').price,
        'interiorCleaningSUVPrice': Pricing.objects.get(name='interiorCleaningSUV').price,
        'BasicExteriorWithinteriorCleaningPrice': Pricing.objects.get(name='BasicExteriorWithinteriorCleaning').price,
        'BasicExteriorWithinteriorCleaningSUVPrice': Pricing.objects.get(name='BasicExteriorWithinteriorCleaningSUV').price,
        'exteriorWashWithWaxPrice': Pricing.objects.get(name='exteriorWashWithWax').price,
        'exteriorWashWithWaxSUVPrice': Pricing.objects.get(name='exteriorWashWithWaxSUV').price,
        'superDirtyExteriorWashPrice': Pricing.objects.get(name='superDirtyExteriorWash').price,
        'superDirtyExteriorWashSUVPrice': Pricing.objects.get(name='superDirtyExteriorWashSUV').price,
        'engineDetailingPrice': Pricing.objects.get(name='engineDetailing').price,
        'engineDetailingSUVPrice': Pricing.objects.get(name='engineDetailingSUV').price,
    }

    if request.method == 'POST':
        # Getting values from form
        basicExteriorWash = int(request.POST['basicExteriorWash'])
        interiorCleaning = int(request.POST['interiorCleaning'])
        BasicExteriorWithinteriorCleaning = int(
            request.POST['BasicExteriorWithinteriorCleaning'])
        exteriorWashWithWax = int(
            request.POST['exteriorWashWithWax'])
        superDirtyExteriorWash = int(
            request.POST['superDirtyExteriorWash'])
        engineDetailing = int(request.POST['engineDetailing'])
        basicExteriorWashSUV = int(request.POST['basicExteriorWashSUV'])
        interiorCleaningSUV = int(request.POST['interiorCleaningSUV'])
        BasicExteriorWithinteriorCleaningSUV = int(
            request.POST['BasicExteriorWithinteriorCleaningSUV'])
        exteriorWashWithWaxSUV = int(
            request.POST['exteriorWashWithWaxSUV'])
        superDirtyExteriorWashSUV = int(
            request.POST['superDirtyExteriorWashSUV'])
        engineDetailingSUV = int(request.POST['engineDetailingSUV'])
        # Checking form input and updating prices
        if interiorCleaning > 0:
            price += (Pricing.objects.get(name='interiorCleaning').price *
                      interiorCleaning)
            description += f'Interior Cleaning = {interiorCleaning}\n'
        if BasicExteriorWithinteriorCleaning > 0:
            price += (Pricing.objects.get(name='BasicExteriorWithinteriorCleaning').price *
                      BasicExteriorWithinteriorCleaning)
            description += f'Basic Exterior With Interior Cleaning = {BasicExteriorWithinteriorCleaning}\n'
        if engineDetailing > 0:
            price += (Pricing.objects.get(name='engineDetailing').price *
                      engineDetailing)
            description += f'Engine Detailing = {engineDetailing}\n'
        if basicExteriorWash > 0:
            price += (Pricing.objects.get(name='basicExteriorWash').price *
                      basicExteriorWash)
            description += f'Basic Exterior Wash = {basicExteriorWash}\n'
        if exteriorWashWithWax > 0:
            price += (Pricing.objects.get(name='exteriorWashWithWax').price *
                      exteriorWashWithWax)
            description += f'Exterior Wash With Wax = {exteriorWashWithWax}\n'
        if superDirtyExteriorWash > 0:
            price += (Pricing.objects.get(name='superDirtyExteriorWash').price *
                      superDirtyExteriorWash)
            description += f'Super Dirty Exterior Wash = {superDirtyExteriorWash}\n'
        if interiorCleaningSUV > 0:
            price += (Pricing.objects.get(name='interiorCleaningSUV').price *
                      interiorCleaningSUV)
            description += f'Interior Cleaning (SUV) = {interiorCleaningSUV}\n'
        if BasicExteriorWithinteriorCleaningSUV > 0:
            price += (Pricing.objects.get(name='BasicExteriorWithinteriorCleaningSUV').price *
                      BasicExteriorWithinteriorCleaningSUV)
            description += f'Basic Exterior With Interior Cleaning = {BasicExteriorWithinteriorCleaningSUV}\n'
        if engineDetailingSUV > 0:
            price += (Pricing.objects.get(name='engineDetailingSUV').price *
                      engineDetailingSUV)
            description += f'Engine Detailing (SUV) = {engineDetailingSUV}\n'
        if basicExteriorWashSUV > 0:
            price += (Pricing.objects.get(name='basicExteriorWashSUV').price *
                      basicExteriorWashSUV)
            description += f'Basic Exterior Wash (SUV) = {basicExteriorWashSUV}\n'
        if exteriorWashWithWaxSUV > 0:
            price += (Pricing.objects.get(name='exteriorWashWithWaxSUV').price *
                      exteriorWashWithWaxSUV)
            description += f'Exterior Wash With Wax (SUV) = {exteriorWashWithWaxSUV}\n'
        if superDirtyExteriorWashSUV > 0:
            price += (Pricing.objects.get(name='superDirtyExteriorWashSUV').price *
                      superDirtyExteriorWashSUV)
            description += f'Super Dirty Exterior Wash (SUV) = {superDirtyExteriorWashSUV}\n'
        # Creating car wash model instance
        newCarWash = Service.objects.create(
            serviceType='cwsh',
            package='one-time',
            price=price,
            description=description,
            autoRenew=False,
        )
        ServiceCarWash.objects.create(
            general=newCarWash,
            basicExteriorWash=basicExteriorWash,
            interiorCleaning=interiorCleaning,
            BasicExteriorWithinteriorCleaning=BasicExteriorWithinteriorCleaning,
            exteriorWashWithWax=exteriorWashWithWax,
            superDirtyExteriorWash=superDirtyExteriorWash,
            engineDetailing=engineDetailing,
            basicExteriorWashSUV=basicExteriorWashSUV,
            interiorCleaningSUV=interiorCleaningSUV,
            BasicExteriorWithinteriorCleaningSUV=BasicExteriorWithinteriorCleaningSUV,
            exteriorWashWithWaxSUV=exteriorWashWithWaxSUV,
            superDirtyExteriorWashSUV=superDirtyExteriorWashSUV,
            engineDetailingSUV=engineDetailingSUV,
        )
        # messages.success(request, f'Service added to cart')
        return redirect('booking', newCarWash.id)
    return render(request, 'services/singleCarService.html', context)


@login_required
def packageCarWashView(request):
    price = 0
    packageName = 'subscription'
    numOfDays = 1

    if request.method == 'POST':

        car_type = request.POST.get('car_select')
        print(car_type)

        if car_type == '':
            messages.error(request, 'Select Car type')
            return redirect('packageCarWash')

        basicExterior = int(
            request.POST['basicExteriorWash'])
        print(basicExterior)
        interiorCleaning = int(
            request.POST['interiorCleaning'])

        if car_type == 'Sedan':
            price += 22 * basicExterior
            price += 15 * interiorCleaning
        elif car_type == 'SUV':
            price += 27 * basicExterior
            price += 17 * interiorCleaning

        if basicExterior == 4:
            numOfDays = 1
        elif basicExterior == 8:
            numOfDays = 2
        elif basicExterior == 12:
            numOfDays = 3

        description = f'Car Type = {car_type}\nExterior Wash = {basicExterior}\nInterior Cleaning = {interiorCleaning}\n'

        newCarWash = Service.objects.create(
            serviceType='cwsh',
            package=packageName,
            price=price,
            numOfDays=numOfDays,
            description=description,
        )

        if car_type == 'Sedan':
            ServiceCarWash.objects.create(
                general=newCarWash,
                basicExteriorWash=basicExterior,
                interiorCleaning=interiorCleaning,
            )
        elif car_type == 'SUV':
            ServiceCarWash.objects.create(
                general=newCarWash,
                basicExteriorWashSUV=basicExterior,
                interiorCleaningSUV=interiorCleaning,

            )
        return redirect('booking', newCarWash.id)
    return render(request, 'services/packageCarService.html')


def PrePurchaseInspectionView(request):

    if request.method == 'POST':

        newinspection = Service.objects.create(
            serviceType='vppi',
            package='one-time',
            price=Pricing.objects.get(name='vppi:carmaintenance').price,
            description='Full Pre-Purchase vehicle inspection for your vehicle\n',
            autoRenew=False,
        )
        return redirect('booking', newinspection.id)

    return render(request, 'services/prePurchaseInspection.html')


def cartView(request):
    cart = None
    totalPrice = 0
    # Checks for anonymous user and gets/creates their cart
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        device = request.COOKIES['device']
        try:
            cart = Cart.objects.get(deviceID=device)
        except:
            cart = Cart.objects.create(deviceID=device)
    services = Service.objects.filter(cartRef=cart)

    for service in services:
        totalPrice += service.price

    carWashes = ServiceCarWash.objects.filter(general__in=services)
    gardens = ServiceGarden.objects.filter(general__in=services)
    houseKeepings = ServiceHouseKeeping.objects.filter(general__in=services)
    vehicleInspections = Service.objects.filter(
        serviceType='vppi', cartRef=cart)
    VehicleMaintenances = Service.objects.filter(
        serviceType='vhmn', cartRef=cart)

    context = {
        'services': services,
        'carWashes': carWashes,
        'gardens': gardens,
        'houseKeepings': houseKeepings,
        'vehicleInspections': vehicleInspections,
        'VehicleMaintenances': VehicleMaintenances,
        'prices': Pricing.objects.all(),
        'totalPrice': totalPrice
    }
    if request.method == 'POST':
        for garden in gardens:
            if 'grdnDel-'+str(garden.id) in request.POST:
                garden.general.delete()
                # messages.success(
                #     request, f'Garden Maintenance item removed from cart')
                return JsonResponse({'msg': 'Garden Maintenance item removed from cart'})
                # return redirect('cart')

        for houseKeeping in houseKeepings:
            if 'hskpDel-'+str(houseKeeping.id) in request.POST:
                houseKeeping.general.delete()
                # messages.success(
                #     request, f'House Keeping item removed from cart')
                return JsonResponse({'msg': 'House Maintenance item removed from cart'})
                # return redirect('cart')

        for vehicleInspection in vehicleInspections:
            if 'vppiDel-'+str(vehicleInspection.id) in request.POST:
                vehicleInspection.delete()
                # messages.success(
                #     request, f'Vehicle Inspection item removed from cart')
                return JsonResponse({'msg': 'Vehicle Inspection item removed from cart'})
                # return redirect('cart')

        for VehicleMaintenance in VehicleMaintenances:
            if 'vhmnDel-'+str(VehicleMaintenance.id) in request.POST:
                VehicleMaintenance.delete()
                # messages.success(
                #     request, f'Vehicle Maintenance item removed from cart')
                return JsonResponse({'msg': 'Vehicle Maintenance item removed from cart'})
                # return redirect('cart')

        for carWash in carWashes:
            if 'cwshDel-'+str(carWash.id) in request.POST:
                # Service.objects.get(id=carWash['general_id']).delete()
                carWash.general.delete()
                # messages.success(
                #     request, f'Car Wash item removed from cart')
                return JsonResponse({'msg': 'Car Wash item removed from cart'})
                # return redirect('cart')
    return render(request, 'services/cart.html', context)


def checkoutAddressView(request):
    addresses = None
    cart = None
    discount = 0
    servicesPrice = 0
    coupon = None
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        addresses = Address.objects.filter(user=request.user)
    else:
        device = request.COOKIES['device']
        cart = Cart.objects.get(deviceID=device)
        addresses = Address.objects.filter(deviceID=device)

    services = Service.objects.filter(cartRef=cart)
    if len(services) == 0:
        messages.error(request, 'No items in cart')
        return redirect('cart')

    for service in services:
        if service.paused:
            servicesPrice += 10
        else:
            servicesPrice += service.price
    serviceVat = float(servicesPrice) * 0.05
    totalPrice = float(servicesPrice) + serviceVat

    context = {
        'addresses': addresses,
        'services': services,
        'servicesPrice': servicesPrice,
        'vat': serviceVat,
        'discount': discount,
        'coupon': coupon,
        'totalPrice': totalPrice,
        'paymentPortal': False
    }

    if request.method == 'POST':
        coupon = None
        # getting the coupon
        if 'couponInput' in request.POST:
            couponID = request.POST['couponInput']
            # checking coupon name
            if couponID != '':
                try:
                    coupon = Coupon.objects.get(name=couponID)
                except:
                    messages.error(request, 'ERROR - incorrect coupon name')
                    return redirect('checkoutAddress')
                # checking how many times this user has used this coupon
                previousCheckouts = Checkout.objects.filter(coupon=coupon)
                if len(previousCheckouts) >= coupon.uses:
                    messages.error(
                        request, 'ERROR - The coupon\'s uses have run out')
                    return redirect('checkoutAddress')
                # Getting the discount that will be applied to services
                couponServicePrice = 0
                if coupon.percentageDiscount:
                    # getting the discount by percentage
                    if coupon.serviceType == 'all':
                        if coupon.onetime and coupon.subscription:
                            couponServicePrice = (float(coupon.discount)
                                                  * servicesPrice) / 100
                        elif coupon.onetime and not coupon.subscription:
                            for service in services:
                                if service.package == 'one-time':
                                    couponServicePrice += service.price
                        elif not coupon.onetime and coupon.subscription:
                            for service in services:
                                if service.package == 'subscription':
                                    couponServicePrice += service.price
                        discount = (float(coupon.discount) *
                                    float(couponServicePrice)) / 100
                    else:
                        for service in services:
                            if service.serviceType == coupon.serviceType:
                                if coupon.onetime and coupon.subscription:
                                    couponServicePrice += service.price
                                elif coupon.onetime and not coupon.subscription:
                                    if service.package == 'one-time':
                                        couponServicePrice += service.price
                                elif not coupon.onetime and coupon.subscription:
                                    if service.package == 'subscription':
                                        couponServicePrice += service.price
                        discount = (float(coupon.discount) *
                                    float(couponServicePrice)) / 100
                    # checking if applying the discount exceeds max discount for the coupon
                    if discount > float(coupon.maxDiscount):
                        discount = float(coupon.maxDiscount)
                else:
                    # getting the discount by cash
                    discount = float(coupon.discount)
                if (totalPrice - discount) < 20:
                    messages.error(
                        request, "ERROR - can't apply coupon for this total")
                    return redirect('checkoutAddress')
                newServicesPrice = 0
                # applying the discount
                if coupon.serviceType == 'all':
                    # applying to all services
                    newServicesPrice = servicesPrice - discount
                else:
                    # applying to specific service
                    difference = float(couponServicePrice) - discount
                    newServicesPrice = float(
                        servicesPrice) - float(couponServicePrice) + difference
                serviceVat = newServicesPrice * 0.05
                totalPrice = float(newServicesPrice) + serviceVat
                context['discount'] = discount
                context['vat'] = serviceVat
                context['totalPrice'] = totalPrice
                context['coupon'] = coupon.name
                if 'paySubmit' not in request.POST:
                    return render(request, 'services/checkoutAddress.html', context)
        # completing the payment
        if 'paySubmit' in request.POST:
            # getting the address
            selectedAddress = request.POST.get('addressInput')
            if selectedAddress == None:
                messages.error(request, f'ERROR - Please select an address')
                return redirect('checkoutAddress')

            # setting the address to string
            addressFinal = None
            for address in addresses:
                if str(address) == selectedAddress:
                    addressFinal = f'Unit No.: {address.unitNo},\nArea: {address.area},\nBuilding Name: {address.buildingName},\nNearest Landmark: {address.nearestLandmark},\nState: {address.state}, \nGoogle Maps: {address.googleMapsLink}'

            email = None
            phone = None
            # deleting address of guest user
            if not request.user.is_authenticated:
                email = request.POST.get('guestEmailInput')
                phone = request.POST.get('guestPhoneInput')
                if email == '' or phone == '':
                    messages.error(
                        request, f'ERROR - Please enter your email and phone number')
                    return redirect('checkoutAddress')
                for address in addresses:
                    address.delete()
            else:
                email = request.user.email
                phone = request.user.phone_number

            cashOnDelivery = request.POST.get('cashOnDelivery')

            # creating the Checkout object
            checkout = Checkout.objects.create(
                email=email,
                phone=phone,
                address=addressFinal,
                servicesPrice=servicesPrice,
                discount=context["discount"],
                vat=context["vat"],
                total=context["totalPrice"],
                coupon=coupon,
                cashOnDelivery=bool(cashOnDelivery),
            )

            # Setting the user value if user is authenticated
            if request.user.is_authenticated:
                checkout.user = request.user
                checkout.save()

            url = "https://business.mamopay.com/manage_api/v1/links"
            if not checkout.cashOnDelivery:
                payload = {
                    "custom_data": {
                        "val1": True,
                        "val2": "custom value"
                    },
                    "name": f"{checkout.id}",
                    "description": "basic exterior wash",
                    "capacity": 1,
                    "active": True,
                    "return_url": f"http://127.0.0.1:8000/services/checkoutPayment/{checkout.id}",
                    "amount": checkout.total,
                    "enable_message": False,
                    "enable_tips": True,
                    "enable_customer_details": True
                }
                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "Authorization": "Token sk-c829bb50-69c5-4a1c-9f65-00f091b6a4a0"
                }
                response = requests.post(url, json=payload, headers=headers)
                jsonResponse = json.loads(response.text)  # string to json
                webbrowser.open(jsonResponse['payment_url'], new=0)
                return redirect('index')
            else:
                return redirect('checkoutPayment', checkout)
    return render(request, 'services/checkoutAddress.html', context)


def checkoutPaymentView(request, pk):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        device = request.COOKIES['device']
        cart = Cart.objects.get(deviceID=device)

    checkout = Checkout.objects.get(id=pk)
    services = Service.objects.filter(cartRef=cart)

    # setting the checkout payed if they come to the page through the payment gateway
    if not checkout.cashOnDelivery:
        checkout.payed = True
        checkout.save()

    # deleting expired bookings made when the service was added to the cart
    bookings = Booking.objects.filter(service__in=services)
    for booking in bookings:
        if booking.date <= datetime.now().date():
            booking.delete()

    # removing services from cart and adding their checkout reference
    for service in services:
        service.checkoutRef = checkout
        service.cartRef = None
        service.save()

    try:
        # sending the invoice email
        subject = f'Rapid Care Invoice #{checkout.id}'
        customer = [f'{checkout.email}']
        msg = emailInvoice(checkout, services)
        mail = EmailMultiAlternatives(
            subject,
            body=msg,
            from_email=EMAIL_HOST_USER,
            to=customer
        )
        mail.attach_alternative(msg, "text/html")
        mail.mixed_subtype = 'related'
        mail.attach(img_data('images/rapid_care_logo.png', '<logo>'))
        mail.attach(img_data('images/rapid care invoice sign.png', '<sign>'))
        mail.send()
    except:
        messages.error(request, 'Email not send')
        return redirect('index')

    try:
        # sending the invoice email to admin
        subject = f'Rapid Care Invoice #{checkout.id}'
        customer = [f'{EMAIL_HOST_USER}']
        msg = f'''This Order has been made to an following address <br><br>'''
        address = checkout.address.split('\n')
        for i in address:
            msg += f'{i} <br>'
        msg += emailInvoice(checkout, services)
        mail = EmailMultiAlternatives(
            subject,
            body=msg,
            from_email=EMAIL_HOST_USER,
            to=customer
        )
        mail.attach_alternative(msg, "text/html")
        mail.mixed_subtype = 'related'
        mail.attach(img_data('images/rapid_care_logo.png', '<logo>'))
        mail.attach(img_data('images/rapid care invoice sign.png', '<sign>'))
        mail.send()
    except:
        print('error')

    messages.info(
        request, f'Invoice #{checkout.id} has been emailed to this account\'s mail')
    return redirect('index')


def bookingView(request, pk):
    cart = None
    # Checks for anonymous user and gets/creates their cart
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        device = request.COOKIES['device']
        try:
            cart = Cart.objects.get(deviceID=device)
        except:
            cart = Cart.objects.create(deviceID=device)
    service = Service.objects.get(id=pk)
    maxServiceTimes = Worker.objects.get(
        serviceType=service.serviceType).numOfWorkers

    print(maxServiceTimes)
    serviceTimes = {
        '08': True,
        '10': True,
        '15': True,
        '17': True,
        '19': True,
        '21': True,
    }
    weekDays = [['sun', serviceTimes], ['mon', serviceTimes], ['tue', serviceTimes], [
        'wed', serviceTimes], ['thu', serviceTimes], ['fri', serviceTimes], ['sat', serviceTimes]]
    times = [8, 10, 15, 17, 19, 21]

    # Checking the number of Days left in a month (Function Starts)
    dt = date.today()
    res = calendar.monthrange(dt.year, dt.month)
    de = date(dt.year, dt.month, res[1])
    rangeDate = int(de.day) - int(dt.day)  # Getting the days in the month left

    curr = datetime.now().date()

    days = [[curr, ], ]
    for i in range(rangeDate):
        curr += timedelta(days=1)
        days.append([curr, ])

    dayTimes = {}
    for day in days:
        for time in times:
            dayTimes.update({time: 0})
        day.append(dayTimes)

    bookings = []
    for day in days:
        bookingDay = Booking.objects.filter(date=day[0])
        for booking in bookingDay:
            if booking.service.serviceType == service.serviceType:
                bookings.append((day[0], booking.time))

    for i in bookings:
        for j in days:
            if i[0] == j[0]:
                new = deepcopy(j)
                new[1].update({i[1]: bookings.count(i)})
                # print(j)
                j[1] = new[1]

    # Checking the number of Days left in a month (Function End)

    # Setting Days for the next month (Function Starts)
    nextMonthStart = None
    nextMonthEnd = None
    monthDays = None
    startDate = None
    if date.today().month == 12:
        year = date.today().year + 1
        nextMonthStart = date(year, 1, 1)
        res = calendar.monthrange(nextMonthStart.year, nextMonthStart.month)
        nextMonthEnd = date(nextMonthStart.year, nextMonthStart.month, res[1])
        # Getting the days in the month left
        monthDays = int(nextMonthEnd.day) - int(nextMonthStart.day)
        startDate = datetime.date(year, 1, 1)

    else:
        month = date.today().month + 1
        nextMonthStart = date(date.today().year, month, 1)
        res = calendar.monthrange(nextMonthStart.year, nextMonthStart.month)
        nextMonthEnd = date(nextMonthStart.year, nextMonthStart.month, res[1])
        # Getting the days in the month left
        monthDays = int(nextMonthEnd.day) - int(nextMonthStart.day)
        startDate = datetime(date.today().year, month, 1)

    nextMonthDays = [[startDate, ], ]
    for i in range(monthDays):
        startDate += timedelta(days=1)
        nextMonthDays.append([startDate, ])

    dayTimes = {}
    for day in nextMonthDays:
        for time in times:
            dayTimes.update({time: 0})
        day.append(dayTimes)

    bookings = []
    for day in nextMonthDays:
        bookingDay = Booking.objects.filter(date=day[0])
        for booking in bookingDay:
            if booking.service.serviceType == service.serviceType:
                bookings.append((day[0], booking.time))

    for i in bookings:
        for j in nextMonthDays:
            if i[0] == j[0]:
                new = deepcopy(j)
                new[1].update({i[1]: bookings.count(i)})
                j[1] = new[1]

    # Setting Days for the next month (Function Ends)

    # Package Booking Days (Function Starts)
    packageBookings = []  # to store the already made bookings
    curr = date.today()
    packageRange = calendar.monthrange(curr.year, curr.month)
    dateRange = packageRange[1]

    packageDays = [[curr,], ]  # storing dates in list
    for i in range(dateRange):
        curr += timedelta(days=1)
        packageDays.append([curr,])

    for day in packageDays:
        monthbookingDay = Booking.objects.filter(date=day[0])
        for booking in monthbookingDay:
            if booking.service.serviceType == service.serviceType:
                packageBookings.append((day[0], booking.time))

    # Storing the datetime for already booked slots
    duplicates = [booking for booking in packageBookings if packageBookings.count(
        booking) >= maxServiceTimes]
    unique_duplicates = list(set(duplicates))

    # Storing weekday and time of already booked slot
    availableTimes = []
    for i in unique_duplicates:
        availableTimes.append([i[0].strftime('%w'), i[1]])

    # Setting the times of the weekday to false for slots which have already been booked
    for i in availableTimes:
        new = deepcopy(weekDays[int(i[0])][1])
        new.update({str(i[1]): False})
        weekDays[int(i[0])][1] = new

    # Package Booking Days (Function Ends)

    print('Max Bookings allowed', service.numOfDays)

    context = {
        'service': service,
        'times': serviceTimes,
        'days': days,
        'nextMonthDays': nextMonthDays,
        'weekDays': weekDays,
        'maxServiceTimes': maxServiceTimes,
        'numOfDays': service.numOfDays
    }

    if request.method == 'POST':
        if service.package == 'subscription':
            start = packageDays[0][0]
            end = packageDays[-1][0]
            sun = bool(request.POST.get('sun'))
            mon = bool(request.POST.get('mon'))
            tue = bool(request.POST.get('tue'))
            wed = bool(request.POST.get('wed'))
            thu = bool(request.POST.get('thu'))
            fri = bool(request.POST.get('fri'))
            sat = bool(request.POST.get('sat'))
            timesun = int(request.POST.get('suntimings'))
            timemon = int(request.POST.get('montimings'))
            timetue = int(request.POST.get('tuetimings'))
            timewed = int(request.POST.get('wedtimings'))
            timethu = int(request.POST.get('thutimings'))
            timefri = int(request.POST.get('fritimings'))
            timesat = int(request.POST.get('sattimings'))

            count = 0
            for day in weekDays:
                if bool(request.POST.get(day[0])):
                    count += 1
            if count != service.numOfDays:
                messages.error(
                    request, f'ERROR - please choose {service.numOfDays} days')
                return redirect('booking', pk)

            # updating previous days, if user comes back to booking screen
            try:
                serviceDays = Days.objects.get(service=service)
                serviceDays.delete()
            except:
                Days.objects.create(
                    service=service,
                    sun=sun,
                    mon=mon,
                    tue=tue,
                    wed=wed,
                    thu=thu,
                    fri=fri,
                    sat=sat
                )

            curr = []

            service.description += f'Booking: ('

            if sun:
                curr.append(pd.date_range(start=start, end=end,
                                          freq='W-SUN').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timesun))
                del curr[-1]
                curr.extend(temp)

                service.description += f'Sunday: {timesun}:00, '

            if mon:
                curr.append(pd.date_range(start=start, end=end,
                                          freq='W-MON').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timemon))
                del curr[-1]
                curr.extend(temp)

                service.description += f'Monday: {timemon}:00, '

            if tue:
                curr.append(pd.date_range(start=start, end=end,
                                          freq='W-TUE').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timetue))
                del curr[-1]
                curr.extend(temp)

                service.description += f'Tuesday: {timetue}:00, '

            if wed:
                curr.append(pd.date_range(start=start, end=end,
                                          freq='W-WED').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timewed))
                del curr[-1]
                curr.extend(temp)

                service.description += f'Wednesday: {timewed}:00, '

            if thu:
                curr.append(pd.date_range(start=start, end=end,
                                          freq='W-THU').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timethu))
                del curr[-1]
                curr.extend(temp)

                service.description += f'Thursday: {timethu}:00, '

            if fri:
                curr.append(pd.date_range(start=start, end=end,
                                          freq='W-FRI').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timefri))
                del curr[-1]
                curr.extend(temp)

                service.description += f'Friday: {timefri}:00, '

            if sat:
                curr.append(pd.date_range(start=start, end=end,
                                          freq='W-SAT').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timesat))
                del curr[-1]
                curr.extend(temp)

                service.description += f'Saturday: {timesat}:00, '
            service.description += ')'
            # updating previous bookings, if user comes back to booking screen
            previousBookings = Booking.objects.filter(service=service)
            if len(previousBookings) > 0:
                for previous in previousBookings:
                    previous.delete()
            for dateTime in curr:
                Booking.objects.create(
                    service=service,
                    date=dateTime[0],
                    time=dateTime[1],
                )
        else:
            start = request.POST.get('startDate')
            onetime = request.POST.get('onetimings')
            if onetime == '':
                messages.error(request, 'ERROR - Select a booking time')
                return redirect('booking', pk)
            end = start
            try:
                previous = Booking.objects.get(service=service)
                previous.date = start
                previous.time = int(onetime)
                previous.save()
            except:
                Booking.objects.create(
                    service=service,
                    date=start,
                    time=int(onetime),
                )
            service.description += f'Booking: ({start}: {onetime}:00)'

        service.startDate = start
        service.endDate = end

        if service.checkoutRef == None:
            service.cartRef = cart
            service.save()
            messages.success(request, 'Service added to cart')
            return redirect('cart')
        else:
            service.paused = False
            service.save()
            messages.success(request, 'New service booking timings set')
            return redirect('profile')
    return render(request, 'services/booking.html', context)


def VehicleMaintenanceView(request):
    cars = CarData.objects.all()
    carMakes = []
    for car in cars:
        if car.make not in carMakes:
            carMakes.append(car.make)
    years = []
    [years.append(i) for i in range(2000, date.today().year)]
    context = {
        'carMakes': carMakes,
        'carModels': None,
        'years': years,
    }
    make = None
    model = None
    if request.method == 'POST':

        make = request.POST['make']

        if 'makeSubmit' in request.POST:
            context['carModels'] = CarData.objects.filter(
                make=make).values_list('carModel', flat=True)
            context.update({'make': make})
            return render(request, 'services/vehicleMaintenance.html', context)
        if 'modelSubmit' in request.POST:
            try:
                model = request.POST['model']
                year = request.POST['year']
                
                context.update({'price': CarData.objects.get(
                    make=make, carModel=model).price})
                context['make'] = make
                context.update({'model': model})
                context.update({'year': year})
                return render(request, 'services/vehicleMaintenance.html', context)
            except:
                messages.error(request, 'Enter the correct Car details')
                return redirect('vehiclemaintenance')
        if 'priceSubmit':
            model = request.POST['model']
            year = request.POST['year']
            new = Service.objects.create(
                serviceType='vhmn',
                package='one-time',
                price=CarData.objects.get(make=make, carModel=model).price,
                description=f'Brand: {make}\nModel: {model}\n Year: {year}',
                autoRenew=False,
            )
            return redirect('booking', new.id)
    return render(request, 'services/vehicleMaintenance.html', context)
