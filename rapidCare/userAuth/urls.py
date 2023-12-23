from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.indexView, name='index'),
    path('register/', views.userRegistrationView, name='register'),
    path('login/', views.userLoginView, name='login'),
    path('logout/', views.userLogoutView, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='userAuth/password-reset.html'), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='userAuth/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='userAuth/password-reset-confirm.html'), name='password_reset_confirm'),
    path('profile/', views.profileView, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('newAddress/', views.addressCreateView, name='addressCreate'),
    path('addresses/address<int:pk>',
         views.addressUpdateView, name='addressUpdate'),
    path('checkoutList/', views.checkoutListView, name='checkoutList'),
    path('checkoutDetail/<str:pk>',
         views.checkoutDetailView, name='checkoutDetail'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
