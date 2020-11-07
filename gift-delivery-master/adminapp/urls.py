from django.urls import path
from . import views

urlpatterns = [
    path('paynow/<int:id>',views.paynow),
    path('payment/',views.payment),
]
