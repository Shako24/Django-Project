from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
# from rapidCare.settings import EMAIL_HOST_USER
from userAuth.forms import (
    CustomUserRegister,
    CustomUserLogin,
    CustomUserUpdateForm,
    ProfileUpdateForm,
    AddressForm
)
from userAuth.models import CustomUser, Address
from userAuth.email_helper import img_data, emailInvoice, emailSignup
from django.http import JsonResponse
from services.models import Checkout, Service, Booking
from phonenumber_field.phonenumber import PhoneNumber


# Create your views here.

# Index page
def indexView(request):
    return render(request, 'userAuth/index.html')

# User registration form


def userRegistrationView(request):
    context = {'form': CustomUserRegister}
    if request.method == 'POST':
        form = CustomUserRegister(request.POST)
        if form.is_valid():
            user = form.save()
            # sending the signup email
            subject = f'Message from the Founder of Rapid Care UAE'
            customer = [f'{user.email}']
            msg = emailSignup()
            mail = EmailMultiAlternatives(
                subject,
                body=msg,
                from_email=EMAIL_HOST_USER,
                to=customer
            )
            mail.attach_alternative(msg, "text/html")
            mail.mixed_subtype = 'related'
            mail.attach(img_data('images/singupEmail.png', '<signup>'))
            mail.send()
            messages.success(
                request, f'Registered as {user.username} successfully')
        else:
            # for msg in form.error_messages:
            #     messages.error(
            #         request, f"{msg}: {form.error_messages[msg]}"
            #     )

            if CustomUser.objects.get(username=request.POST.get('username')):
                messages.error(request, 'User already exist')

            if request.POST.get('password1') != request.POST.get('password2'):
                messages.error(request, 'Password doesnot match')

        return redirect('login')
    else:
        form = CustomUserRegister()
    return render(request, 'userAuth/login.html', context)

# User login form


def userLoginView(request):
    context = {
        'loginForm': CustomUserLogin,
        'registerForm': CustomUserRegister
    }
    if request.method == 'POST':
        username = request.POST.get('username')

        # if prefix == None or number == None:
        #     username = request.POST.get('username')
        # else:
        #     try:
        #         phone = PhoneNumber.from_string(
        #             phone_number=number, region=prefix).as_e164
        #     except:
        #         messages.error(request, 'ERROR - Invalid phone number')
        #         return redirect('login')

        # if phone != None:
        #     try:
        #         user = CustomUser.objects.get(phone_number=phone)
        #     except:
        #         messages.error(request, 'ERROR - User doesn\'t exist')
        #         return redirect('login')
        #     check = user.check_password(request.POST['password'])
        #     if check == True:
        #         login(request, user,
        #               backend='django.contrib.auth.backends.ModelBackend')
        #         messages.success(
        #             request, f'Logged in as {user.username} successfully')
        #         return redirect('index')
        #     messages.error(request, 'ERROR - Incorrect password')
        #     context = {
        #         'loginForm': CustomUserLogin(request.POST),
        #         'registerForm': CustomUserRegister
        #     }
        #     return render(request, 'userAuth/login.html', context)
        # else:
        try:
            user = CustomUser.objects.get(username=username)
        except:
            messages.error(request, 'ERROR - User doesn\'t exist')
            return redirect('login')
        check = user.check_password(request.POST['password'])
        if check == True:
            login(request, user,
                  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(
                request, f'Logged in as {user.username} successfully')
            return redirect('index')
        messages.error(request, 'ERROR - Incorrect password')
        context = {
            'loginForm': CustomUserLogin(request.POST),
            'registerForm': CustomUserRegister
        }
        return render(request, 'userAuth/login.html', context)

    return render(request, 'userAuth/login.html', context)


def userLogoutView(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('index')


# Profile view
@login_required
def profileView(request):
    # Getting user's addresses, previous checkouts and current subscriptions
    addresses = Address.objects.filter(user=request.user.id)
    transactions = Checkout.objects.filter(
        user=request.user).order_by('-datetime')
    subscriptions = Service.objects.filter(
        package='subscription', checkoutRef__in=transactions),

    if request.method == 'POST':
        userForm = CustomUserUpdateForm(request.POST, instance=request.user)
        imgForm = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)

        # removing addresses
        for address in addresses:
            if 'removeAddress-'+str(address.id) in request.POST:
                address.delete()
                messages.success(request, 'Successfully removed address')

        for subs in subscriptions:
            for sub in subs:
                # removing subscriptions
                if 'removeSub-'+str(sub.id) in request.POST:
                    sub.delete()
                    messages.success(request, f'Subscription removed')
                # pausing subscriptions
                if 'pauseSub-'+str(sub.id) in request.POST:
                    if sub.paused:
                        messages.warning(
                            request, 'Please select booking times')
                        return redirect('booking', sub.id)

                    bookings = Booking.objects.filter(service=sub)
                    [booking.delete() for booking in bookings]
                    sub.paused = True
                    sub.save()
                    messages.success(
                        request, f'Subscription paused and bookings cancelled')
                if 'renewSub-'+str(sub.id) in request.POST:
                    if sub.autoRenew:
                        sub.autoRenew = False
                        sub.save()
                        messages.success(
                            request, 'Subscription auto renew is disabled')

                    else:
                        sub.autoRenew = True
                        sub.save()
                        messages.success(
                            request, 'Subscription auto renew is enabled')

        # updating user info
        if userForm.is_valid():
            userForm.save()
            messages.success(request, f'Account Info Updated!')
            return redirect('profile')

        # updating profile pic
        if imgForm.is_valid():
            imgForm.save()
            messages.success(request, f'Profile Updated!')
            return redirect('profile')
        messages.error(request, f'Profile pic not updated')

    else:
        # displaying user info
        userForm = CustomUserUpdateForm(instance=request.user)
        imgForm = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Profile',
        'userForm': userForm,
        'imgForm': imgForm,
        'addresses': Address.objects.filter(user=request.user.id),
        'subscriptions': Service.objects.filter(package='subscription', checkoutRef__in=transactions),
        'transactions': transactions,
    }
    return render(request, 'userAuth/profile.html', context)


# View for adding new address
# @login_required
def addressCreateView(request):
    context = {
        'addressForm': AddressForm(),
        'display': 'Your Location',
        'mLat': 0,
        'mLng': 0,
    }
    if request.method == 'POST':
        if request.user.is_authenticated:
            currentAddresses = Address.objects.filter(user=request.user)
            if len(currentAddresses) == 5:
                messages.error(
                    request, 'You have reached the max number of addresses. Remove one to create a new one')
                return redirect('profile')
        addressForm = AddressForm(request.POST)
        if addressForm.is_valid():
            if request.POST['lat_lng'] == 'None':
                context = {
                    'addressForm': AddressForm(request.POST),
                    'display': 'Your Location',
                    'mLat': 0,
                    'mLng': 0,
                }
                messages.error(request, 'Map location is required')
                return render(request, 'userAuth/addressDetail.html', context)
            latlng = request.POST['lat_lng'].split(',')
            lat = latlng[0][1:]
            lng = latlng[1][1:-1]
            newAddress = Address.objects.create(
                # user=request.user,
                state=addressForm.data['state'],
                area=addressForm.data['area'],
                unitNo=addressForm.data['unitNo'],
                buildingName=addressForm.data['buildingName'],
                nearestLandmark=addressForm.data['nearestLandmark'],
                mapLatLng=request.POST['lat_lng'],
                googleMapsLink=f'http://www.google.com/maps/place/{lat},{lng}',
            )
            if request.user.is_authenticated:
                newAddress.user = request.user
                newAddress.save()
                messages.success(request, 'Successfully created address')
                return redirect('profile')
            else:
                newAddress.deviceID = request.COOKIES['device']
                newAddress.save()
                return redirect('checkout')
    return render(request, 'userAuth/addressDetail.html', context)


def addressUpdateView(request, pk):
    if request.user.is_authenticated:
        addr = Address.objects.get(id=pk, user=request.user)
    else:
        addr = Address.objects.get(id=pk)
    lat = 0
    lng = 0
    if addr.mapLatLng != 'None':
        latlng = addr.mapLatLng.split(',')
        lat = latlng[0][1:]
        lng = latlng[1][1:-1]
    context = {
        'address': pk,
        'addressForm': AddressForm(instance=addr),
        'display': 'Your Location',
        'mLat': float(lat),
        'mLng': float(lng),
    }
    if request.method == 'POST':
        if 'removeAddress' in request.POST:
            addr.delete()
            messages.success(request, 'Successfully removed address')
            if request.user.is_authenticated:
                return redirect('profile')
            else:
                return redirect('checkout')
        addr.mapLatLng = request.POST['lat_lng']
        latlng = addr.mapLatLng.split(',')
        lat = latlng[0][1:]
        lng = latlng[1][1:-1]
        addr.googleMapsLink = f'http://www.google.com/maps/place/{lat},{lng}'
        addr.save()
        updateForm = AddressForm(request.POST, instance=addr)
        updateForm.save()
        messages.success(request, 'Successfully updated address')
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            return redirect('checkout')
    return render(request, 'userAuth/addressDetail.html', context)


@login_required
def checkoutListView(request):
    context = {
        'transactions': Checkout.objects.filter(user=request.user)
    }
    return render(request, 'userAuth/checkoutList.html', context)


@login_required
def checkoutDetailView(request, pk):
    transaction = Checkout.objects.get(id=pk, user=request.user)
    address = transaction.address.split('\n')
    context = {
        'transaction': transaction,
        'address': address,
        'services': Service.objects.filter(checkoutRef=pk)
    }
    return render(request, 'userAuth/checkoutDetail.html', context)


def emailView(request):
    if request.method == 'POST':
        subject = 'Test Mail'
        customer = ['vitovel339@fom8.com']
        # customer = [f'{request.user.email}']
        serviceList = Service.objects.all()
        msg = emailInvoice(request.user, serviceList)
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
        mail.send(fail_silently=False)
    return render(request, 'userAuth/email.html')


# Contact us Page
def contact_us(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        msg = request.POST['msg']
        msg += f'<br><br>Regards<br>{name},<br>{phone}.'
        # sending the CONTACT US email
        subject = f'Contact us Form'
        mail = EmailMultiAlternatives(
            subject,
            body=msg,
            from_email=EMAIL_HOST_USER,
            to=[f'{EMAIL_HOST_USER}']
        )
        mail.attach_alternative(msg, "text/html")
        mail.mixed_subtype = 'related'
        mail.send()

    return render(request, 'userAuth/Contact_us.html')


# 404 error page
def page_not_found_view(request, exception):
    return render(request, 'userAuth/404.html', status=404)
