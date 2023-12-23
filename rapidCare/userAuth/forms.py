from django import forms
from django.contrib.auth.forms import UserCreationForm
from userAuth.models import CustomUser, Profile, Address
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class CustomUserRegister(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number',
                  'password1', 'password2')
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(initial='AE', attrs={'placeholder': 'ex: 5x xxx xxxx'}),
            'password': forms.PasswordInput()
        }


class CustomUserLogin(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['state', 'area', 'unitNo',
                  'buildingName', 'nearestLandmark', ]
