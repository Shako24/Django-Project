from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from userAuth.models import CustomUser, Profile, Address


class CustomUserAdminConfig(UserAdmin):
    readonly_fields = ('id',)
    ordering = ('-date_joined',)
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')


class AddressAdminConfig(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'user', 'state', 'area', 'unitNo')


# Register your models here.
admin.site.register(CustomUser, CustomUserAdminConfig)
admin.site.register(Profile)
admin.site.register(Address, AddressAdminConfig)
