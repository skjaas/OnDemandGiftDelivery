from django.urls import path
from . import views
urlpatterns = [
    
    path('ssignup/', views.ssignup),
    path('sverify/', views.sverify),
    path('sdashboard/', views.sdashboard),
    path('shome/',views.shome),
    path('sorders/', views.sorders),
    path('sproducts/', views.sproducts),
    path('saveseller/',views.saveseller),
    path('sotpverify/',views.sotpverify),
    path('sviewproducts/',views.sviewproducts),
    path('saddproducts/',views.saddproducts),
    path('ssaveproducts/',views.ssaveproducts),
    path('seditproduct/<int:id>',views.seditproduct),
    path('supdateproducts/<int:id>',views.supdateproducts),
    path('sviewdelete/',views.sviewdelete),
    path('sdeleteproduct/<int:id>',views.sdeleteproduct),
    path('svieworder/',views.svieworder),
    path('supdateorders/',views.supdateorders),
    path('supdatestatus/<int:id>/',views.supdatestatus),
    path('supdatenewstatus/<int:id>/',views.supdatenewstatus),
    path('sreports/',views.sreports),
]
