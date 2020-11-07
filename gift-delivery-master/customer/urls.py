from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('csignup/', views.csignup),
    path('cverify/', views.cverify),
    path('savecustomer/',views.savecustomer),
    path('cotpverify/',views.cotpverify),
    path('chome/',views.chome),
    path('zipcode/',views.zipcode),
    path('cviewshopdetails/<int:id>/',views.cviewshopdetails),
    path('cgiftform/<int:id>/',views.cgiftform),
    path('csendgift/',views.csendgift),
    path('csinglepurchase/',views.csinglepurchase),
    path('cmyorders/',views.cmyorders),
    path('cancelorder/<int:id>/',views.cancelorder),
]
