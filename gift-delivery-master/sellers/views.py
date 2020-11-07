from django.shortcuts import render,redirect
from django.http import HttpResponse
from adminapp.models import *
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

def random_with_N_digits(n):
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start,range_end)

def ssignup(request):
    return render(request, 'ssignup.html')
def sverify(request):
    return render(request, 'sverify.html')
def sdashboard(request):
    return render(request, 'sdashboard.html')
def sorders(request):
    return render(request, 'sorders.html')
def sproducts(request):
    return render(request, 'sproducts.html')


def shome(request):
    sel = sellerlogin.objects.last()
    iid = sel.sellerid
    log = login.objects.get(id=iid)
    username = log.username
    sel = sellers.objects.get(username=username)
    sellerid = sel.id
    tbl = orders.objects.all()
    productIDList = []
    orderIDList = []
    for i in tbl:
        productIDList.append(i.cproductid)
        orderIDList.append(i.id)
    sellerIDList = []
    index = 0
    for i in productIDList:
        row = products.objects.get(id=i)
        if row.sellerId == sellerid:
            orderIndex = orderIDList[index]
            orderrow = orders.objects.get(id=orderIndex)
            if orderrow.cstatus != 'Delivered':
                sellerIDList.append(orderrow)
        index+=1
    return render(request,'shome.html',{'tbl':sellerIDList})
   
def saveseller(request):
    if request.method == 'POST':
        sel = sellers()
        log = login()
        username = request.POST.get('username')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        password = request.POST.get('password')
        if login.objects.filter(username=username) or sellers.objects.filter(email=email):
            return render(request,'ssignup.html',{'msg':'User already exist!!!!'})
        sel.username = username
        sel.name = name
        sel.mobile = mobile
        sel.email = email
        sel.address = address
        sel.zipcode = zipcode
        sel.password = password
        log.username = username
        log.password = password
        log.usertype = 'Seller'
        code = random_with_N_digits(6)
        log.code = code
        log.verified = 'pending'
        if password == request.POST.get('cpassword'):
            subject = 'Confirmation Mail'
            message = ' Your Confirmation Code is '+str(code)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
            sel.save()
            log.save()
            sel = sellerlogin()
            row = login.objects.last()
            sel.sellerid = row.id
            sel.save()
            return render(request,'sverify.html',{'msg':'Seller request sent!!!!'})
        else:
            return render(request,'ssignup.html',{'msg':"Password doesn't macthes!!!!!"})

def sotpverify(request):
    if request.method == 'POST':
        coderow = sellerlogin.objects.last()
        rowid = coderow.sellerid
        row = login.objects.get(id=rowid)
        code = row.code
        row.verified = 'verified'
        row.save()
        if request.POST.get('otp')==code:
            return render(request,'home.html')
        else:
            return render(request,'sverify.html',{'msg':'Entered wrong OTP'})
        
def sviewproducts(request):
    sellertbl = sellerlogin.objects.last()
    sellerid = sellertbl.sellerid
    selrows = login.objects.get(id=sellerid)
    username = selrows.username
    sel = sellers.objects.get(username=username)
    sellerid = sel.id
    print('sellerid:',sellerid)
    pro = products.objects.all()
    lst = []
    for i in pro:
        if i.sellerId == sellerid:
            lst.append(i)
    return render(request,'sviewproducts.html',{'pro':lst})

def saddproducts(request):
    return render(request,'saddproducts.html')
def ssaveproducts(request):
    if request.method == 'POST':
        pro = products()
        sel = sellerlogin.objects.last()
        sellerId = sel.sellerid
        row = login.objects.get(id=sellerId)
        sellerusername = row.username
        sel = sellers.objects.get(username=sellerusername)
        pro.sellerId = sel.id
        pro.zipcode = sel.zipcode
        pro.category = request.POST.get('productcategory')
        pro.description = request.POST.get('productdescription')
        pro.name = request.POST.get('productname')
        pro.price = request.POST.get('productprice')
        pro.idealfor = request.POST.get('productidealfor')
        pro.stock = request.POST.get('productstock')
        image = request.FILES['productimage']
        fs = FileSystemStorage()
        photo = fs.save(image.name,image)
        fileurl = fs.url(photo)
        pro.image = fileurl
        pro.save()
        return redirect('/saddproducts/')

def seditproduct(request,id):
    pro = products.objects.get(id=id)
    return render(request,'seditproduct.html',{'pro':pro})

def supdateproducts(request,id):
    pro = products.objects.get(id=id)
    pro.category = request.POST.get('productcategory')
    pro.description = request.POST.get('productdescription')
    pro.name = request.POST.get('productname')
    pro.price = request.POST.get('productprice')
    pro.idealfor = request.POST.get('productidealfor')
    pro.stock = request.POST.get('productstock')
    image = request.FILES['productimage']
    fs = FileSystemStorage()
    photo = fs.save(image.name,image)
    fileurl = fs.url(photo)
    pro.image = fileurl
    pro.save()
    return redirect('/sviewproducts/')

def sviewdelete(request):
    sellertbl = sellerlogin.objects.last()
    sellerid = sellertbl.sellerid
    selrows = login.objects.get(id=sellerid)
    username = selrows.username
    sel = sellers.objects.get(username=username)
    sellerid = sel.id
    pro = products.objects.all()
    lst = []
    for i in pro:
        if i.sellerId == sellerid:
            lst.append(i)
    return render(request,'sviewdelete.html',{'pro':lst})

def sdeleteproduct(request,id):
    pro = products.objects.get(id=id)
    pro.delete()
    return redirect('/sviewdelete/')

def svieworder(request):
    sel = sellerlogin.objects.last()
    iid = sel.sellerid
    log = login.objects.get(id=iid)
    username = log.username
    sel = sellers.objects.get(username=username)
    sellerid = sel.id
    tbl = orders.objects.all()
    productIDList = []
    orderIDList = []
    for i in tbl:
        productIDList.append(i.cproductid)
        orderIDList.append(i.id)
    sellerIDList = []
    index = 0
    for i in productIDList:
        row = products.objects.get(id=i)
        if row.sellerId == sellerid:
            orderIndex = orderIDList[index]
            orderrow = orders.objects.get(id=orderIndex)
            sellerIDList.append(orderrow)
        index+=1
    return render(request,'svieworder.html',{'tbl':sellerIDList})

def supdateorders(request):
    sel = sellerlogin.objects.last()
    iid = sel.sellerid
    log = login.objects.get(id=iid)
    username = log.username
    sel = sellers.objects.get(username=username)
    sellerid = sel.id
    tbl = orders.objects.all()
    productIDList = []
    orderIDList = []
    for i in tbl:
        productIDList.append(i.cproductid)
        orderIDList.append(i.id)
    sellerIDList = []
    index = 0
    for i in productIDList:
        row = products.objects.get(id=i)
        if row.sellerId == sellerid:
            orderIndex = orderIDList[index]
            orderrow = orders.objects.get(id=orderIndex)
            if orderrow.cstatus != 'Delivered':
                if orderrow.cstatus != 'Canceled':
                    sellerIDList.append(orderrow)
        index+=1
    return render(request,'seditviews.html',{'tbl':sellerIDList})

def supdatestatus(request,id):
    row = orders.objects.get(id=id)
    scurrentstatus = row.cstatus
    return render(request,'supdatestatus.html',{'scurrentstatus':scurrentstatus,'id':id})

def supdatenewstatus(request,id):
    if request.method == 'POST':
        status = request.POST.get('status')
        row = orders.objects.get(id=id)
        row.cstatus = status
        row.save()
        sel = sellerlogin.objects.last()
        iid = sel.sellerid
        log = login.objects.get(id=iid)
        username = log.username
        sel = sellers.objects.get(username=username)
        sellerid = sel.id
        tbl = orders.objects.all()
        productIDList = []
        orderIDList = []
        for i in tbl:
            productIDList.append(i.cproductid)
            orderIDList.append(i.id)
        sellerIDList = []
        index = 0
        for i in productIDList:
            row = products.objects.get(id=i)
            if row.sellerId == sellerid:
                orderIndex = orderIDList[index]
                orderrow = orders.objects.get(id=orderIndex)
                if orderrow.cstatus != 'Delivered':
                    if orderrow.cstatus != 'Canceled':
                        sellerIDList.append(orderrow)
            index+=1
        return render(request,'seditviews.html',{'tbl':sellerIDList})

def sreports(request):
    sel = sellerlogin.objects.last()
    iid = sel.sellerid
    log = login.objects.get(id=iid)
    username = log.username
    sel = sellers.objects.get(username=username)
    sellerid = sel.id
    tbl = orders.objects.all()
    productIDList = []
    orderIDList = []
    for i in tbl:
        productIDList.append(i.cproductid)
        orderIDList.append(i.id)
    sellerIDList = []
    index = 0
    total = 0
    for i in productIDList:
        row = products.objects.get(id=i)
        if row.sellerId == sellerid:
            orderIndex = orderIDList[index]
            orderrow = orders.objects.get(id=orderIndex)
            if orderrow.cstatus == 'Delivered':
                total+=orderrow.camount
                sellerIDList.append(orderrow)
        index+=1
    return render(request,'sreport.html',{'tbl':sellerIDList,'total':total})