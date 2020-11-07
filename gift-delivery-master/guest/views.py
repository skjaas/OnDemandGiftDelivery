from django.shortcuts import render,redirect
from django.http import HttpResponse
from adminapp.models import *

# Create your views here.
def home(request):
    return render(request,'home.html')

def loginlog(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if login.objects.filter(username=username) and login.objects.filter(password=password):
            row = login.objects.get(username=username)
            if row.usertype == 'Seller':
                if row.verified == 'verified':
                    sel = sellerlogin()
                    sel.sellerid = row.id
                    sel.save()
                    return redirect('/shome/')
                else:
                    sel = sellerlogin()
                    sel.sellerid = row.id
                    sel.save()
                    return render(request,'sverify.html')
            else:
                if row.verified == 'verified':
                    cus = customerlogin()
                    cus.customerid = row.id
                    cus.save()
                    return render(request,'chome.html')
                else:
                    cus = customerlogin()
                    cus.customerid = row.id
                    cus.save()
                    return render(request,'cverify.html')
        else:
            return render(request,'home.html',{'msg':"Invalid User"})

def logout(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return render(request,'home.html')
    