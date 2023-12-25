import calendar
from datetime import datetime, date, timedelta
from turtle import pd
from apscheduler.schedulers.background import BackgroundScheduler
from services.models import Cart, Service, Booking, Checkout, Days


# removes guest user carts after 20 days of inception
def cleanCart():
    carts = Cart.objects.all()
    now = datetime.now()
    for cart in carts:
        if cart.user == None:
            if (cart.dateCreated.day - now.day) > 20:
                services = Service.objects.filter(cartRef=cart)
                for service in services:
                    service.delete()
                print(
                    f'scheduler deleted expired cart: -> {cart} and all dependent services')
                cart.delete()


# removes bookings that have expired
def cleanBooking():
    for booking in Booking.objects.all():
        if booking.date < datetime.now().date():
            print(f'scheduler deleted expired booking -> {booking}')
            booking.delete()


# removes incomplete Service instances, where instance was made, but booking process not complete
def cleanService():
    services = Service.objects.filter(cartRef=None, checkoutRef=None)
    for service in services:
        print(f'scheduler deleted incomplete service -> {service}')
        service.delete()


# removes incomplete Checkout instances, where the cashOnDelivery is false and payed is also false
def cleanCheckout():
    checkouts = Checkout.objects.filter(cashOnDelivery=False, payed=False)
    for checkout in checkouts:
        print(f'scheduler deleted incomplete checkout -> {checkout}')
        checkout.delete()


# auto renew feature for services
def autoRenewService():
    services = Service.objects.filter(autoRenew=True)

    for service in services:
        if datetime.now() == service.endDate:
            
            # Setting Days for the next month (Function Starts)
            nextMonthStart = None
            nextMonthEnd = None
            startDate = None
            monthDays = calendar.monthrange(date.today().year, date.today().month)
            if date.today().month == 12:
                year = date.today().year + 1
                nextMonthStart = date(date.today().year, date.today().month, date.today().day+1)
                nextMonthEnd = date(year, 1, date.today().day)
                # Getting the start date of next month subscription
                startDate = date.today() + timedelta(days=1)

            else:
                month = date.today().month + 1
                nextMonthStart = date(date.today().year, date.today().month, date.today().day+1)
                nextMonthEnd = date(nextMonthStart.year, month, date.today().day)
                # Getting the start date of next month subscription
                startDate = date.today() + timedelta(days=1)

            nextMonthDays = [[startDate, ], ]
            for i in range(monthDays[1]):
                startDate += timedelta(days=1)
                nextMonthDays.append([startDate, ])

            serviceDays = Days.objects.get(service=service)

            timesun = 0
            timemon = 0
            timetue = 0
            timewed = 0
            timethu = 0
            timefri = 0
            timesat = 0

            serviceTimes = Booking.objects.filter(service=service)

            for time in serviceTimes:
                if time.weekDay() ==  0:
                    timemon = time.time
                if time.weekDay() ==  1:
                    timetue = time.time
                if time.weekDay() ==  2:
                    timewed = time.time
                if time.weekDay() ==  3:
                    timethu = time.time
                if time.weekDay() ==  4:
                    timefri = time.time
                if time.weekDay() ==  5:
                    timesat = time.time
                if time.weekDay() ==  6:
                    timesun = time.time
                

            curr = []
            if serviceDays.sun:
                curr.append(pd.date_range(start=nextMonthStart, end=nextMonthEnd,
                                          freq='W-SUN').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timesun))
                del curr[-1]
                curr.extend(temp)

            if serviceDays.mon:
                curr.append(pd.date_range(start=nextMonthStart, end=nextMonthEnd,
                                          freq='W-MON').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timemon))
                del curr[-1]
                curr.extend(temp)

            if serviceDays.tue:
                curr.append(pd.date_range(start=nextMonthStart, end=nextMonthEnd,
                                          freq='W-TUE').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timetue))
                del curr[-1]
                curr.extend(temp)

            if serviceDays.wed:
                curr.append(pd.date_range(start=nextMonthStart, end=nextMonthEnd,
                                          freq='W-WED').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timewed))
                del curr[-1]
                curr.extend(temp)

            if serviceDays.thu:
                curr.append(pd.date_range(start=nextMonthStart, end=nextMonthEnd,
                                          freq='W-THU').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timethu))
                del curr[-1]
                curr.extend(temp)

            if serviceDays.fri:
                curr.append(pd.date_range(start=nextMonthStart, end=nextMonthEnd,
                                          freq='W-FRI').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timefri))
                del curr[-1]
                curr.extend(temp)

            if serviceDays.sat:
                curr.append(pd.date_range(start=nextMonthStart, end=nextMonthEnd,
                                          freq='W-SAT').strftime('%Y-%m-%d').tolist())
                temp = []
                for i in curr[-1]:
                    temp.append((i, timesat))
                del curr[-1]
                curr.extend(temp)

            service.startDate = nextMonthStart
            service.endDate = nextMonthEnd
            service.save()

            for dateTime in curr:
                Booking.objects.create(
                    service=service,
                    date=dateTime[0],
                    time=dateTime[1],
                )



            user = Checkout.objects.get(user=service.checkoutRef.user)
            price = user.servicesPrice

            if service.paused:
                price = 10


            checkout = Checkout.objects.create(
                user=user.user,
                email=user.email,
                phone=user.phone,
                address=user.address,
                servicesPrice=price,
                discount=user.discount,
                vat=user.vat,
                total=user.total,
                coupon=user.coupon,
                cashOnDelivery=user.cashOnDelivery,
            )

            service.checkoutRef = checkout
            service.save()



            



# scheduler function
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanCart, 'interval', days=2)
    scheduler.add_job(cleanBooking, 'interval', days=1)
    scheduler.add_job(cleanService, 'interval', days=1)
    scheduler.add_job(cleanCheckout, 'interval', days=1)
    scheduler.add_job(autoRenewService, 'interval', days=1)
    scheduler.start()
