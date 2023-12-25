from django.urls import path
from . import views

urlpatterns = [
    path('', views.servicesView, name='services'),
    path('garden/', views.gardenView, name='garden'),
    path('carWash/', views.carWashView, name='carWash'),
    path('insurance/', views.vehicleInsuranceView, name='vehicleInsurance'),
    path('carWash/single', views.singleCarWashView, name='singleCarWash'),
    path('carWash/package', views.packageCarWashView, name='packageCarWash'),
    path('houseKeeping/', views.houseKeepingView, name='houseKeeping'),
    path('booking/<int:pk>', views.bookingView, name='booking'),
    path('houseKeeping/one-time', views.houseKeepingSingleView,
         name='houseKeepingSingle'),
    path('houseKeeping/package', views.houseKeepingPackageView,
         name='houseKeepingPackage'),
    path('cart/', views.cartView, name='cart'),
    path('checkout/', views.checkoutView, name='checkout'),
    path('checkoutAddress/', views.checkoutAddressView, name='checkoutAddress'),
    path('checkoutPayment/<str:pk>',
         views.checkoutPaymentView, name='checkoutPayment'),
    path('vehicle-care/', views.vehicleCareView, name='vehiclecare'),
    path('vehicle-care/vehicle-maintenance/',
         views.VehicleMaintenanceView, name='vehiclemaintenance'),
    path('vehicle-care/pre-purchase-inspection/', views.PrePurchaseInspectionView,
         name='prepurchaseinspection'),
]
