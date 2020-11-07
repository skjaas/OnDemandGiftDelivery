from django.shortcuts import render,redirect
from django.http import HttpResponse
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from datetime import *
from adminapp.models import *

# Create your views here.

def random_with_N_digits(n):
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start,range_end)
def home(request):
    return render(request, 'home.html')
def csignup(request):
    return render(request, 'csignup.html')
def cverify(request):
    return render(request, 'cverify.html')
def chome(request):
    return render(request,'chome.html')
def savecustomer(request):
    if request.method == 'POST':
        cus = customers()
        log = login()
        name = request.POST.get('name')
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cus.name = name
        cus.username = username
        cus.mobile = mobile
        cus.email = email
        log.username = username
        log.password = password
        log.usertype = 'Customer'
        code = random_with_N_digits(6)
        log.code = code
        log.verified = 'Pending'
        if customers.objects.filter(email=email) or login.objects.filter(username=username):
            return render(request,'csignup.html',{'msg':'User already exist!!!'})
        if password == request.POST.get('cpassword'):
            subject = 'Confirmation Mail'
            message = ' Your Confirmation code is '+str(code)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
            cus.save()
            log.save()
            cus = customerlogin()
            row = login.objects.last()
            cus.customerid = row.id
            cus.save()
            return render(request,'cverify.html',{'msg':'Request Sent'})
        else:
            return render(request,'csignup.html',{'msg':"Password doesn't match"})

def cotpverify(request):
    if request.method == 'POST':
        codeid = login.objects.last()
        code = codeid.code
        codeid.save()
        if request.POST.get('otp')==code:
            codeid.verified = 'verified'
            codeid.save()
            return render(request,'chome.html')
        else:
            return render(request,'cverify.html',{'msg':'Entered wrong OTP'})

def zipcode(request):
    if request.method == 'POST':
        zipcode = request.POST.get('zipcode')
        category = request.POST.get('category')
        print('category:',category)
        print('zipcode:',zipcode)
        pro = products.objects.all()
        lst = []
        for i in pro:
            print('id:',i.category)
            if i.zipcode == zipcode and i.category == category:
                lst.append(i.sellerId)
        print('lst:',lst)
        lst = list(dict.fromkeys(lst))
        print('lst:',lst)
        #sel = sellers.objects.all()
        shop = []
        for i in lst:
            print('i:',i)
            shop.append(sellers.objects.get(id=i))
            print('shops',shop)
        return render(request,'cviewshop.html',{'shop':shop,'category':category})

def cviewshopdetails(request,id):
    if request.method == 'POST':
        sellerId = id
        category = request.POST.get('category')
        print('v:',category)
        pro = products.objects.all()
        lst = []
        for i in pro:
            if i.sellerId == sellerId and i.category == category:
                lst.append(i)
        print(lst)
    return render(request,'cshophome.html',{'pro':lst})


def cgiftform(request,id):
    pro = products.objects.get(id=id)
    sellerId = pro.sellerId
    proid = pro.id
    proimage = pro.image
    return render(request,'cgiftform.html',{'proid':proid,'proimage':proimage})

def csendgift(request):
    tbl = orders()
    proid = request.POST.get('proid')
    tbl.customer = request.POST.get('customer')
    tbl.cdate = request.POST.get('cdate')
    tbl.ctime = request.POST.get('ctime')
    prorow = products.objects.get(id=proid)
    tbl.citemname = prorow.name
    tbl.cimage = prorow.image
    price = prorow.price
    tbl.camount = price
    tbl.caddress = request.POST.get('caddress')
    tbl.cstatus = 'pending'
    tbl.cproductid = proid
    sellerId = prorow.sellerId
    tbl.csellerid = sellerId
    ########################
    cus = customerlogin.objects.last()
    custid = cus.customerid
    log = login.objects.get(id=custid)
    username = log.username
    custrow = customers.objects.get(username=username)
    customerId = custrow.id
    tbl.cid = customerId
    tbl.save()
    purchase = orders.objects.last()
    return render(request,'csinglepurchase.html',{'purchase':purchase,'proid':proid})

def csinglepurchase(request):
    purchase = orders.objects.last()
    return render(request,'csinglepurchase.html',{'purchase':purchase})

def cmyorders(request):
    cus = customerlogin.objects.last()
    custid = cus.customerid
    log = login.objects.get(id=custid)
    username = log.username
    custrow = customers.objects.get(username=username)
    customerId = custrow.id
    tbl = orders.objects.all()
    lst = []
    for i in tbl:
        if i.cid == customerId:
            lst.append(i)
    return render(request,'cmyorders.html',{'orders':lst})

def cancelorder(request,id):
    row = orders.objects.get(id=id)
    if row.cstatus == 'Pending' or row.cstatus == 'Order Accepted':
        pid = row.cproductid
        row.cstatus = 'Canceled'
        row.save()
        pro = products.objects.get(id=pid)
        stock = pro.stock
        pro.stock = stock+1
        pro.save()
    return redirect('/cmyorders/')