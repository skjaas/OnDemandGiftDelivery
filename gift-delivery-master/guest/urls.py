from django.urls import *
from . import views

urlpatterns = [
    path('home/',views.home),
    path('loginlog/',views.loginlog),
    path('logout/',views.logout),
]
