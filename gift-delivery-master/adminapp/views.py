from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from adminapp.models import *

# Create your views here.
def paynow(request,id):
    return render(request,'payment.html',{'id':id})

def payment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cardnumber = request.POST.get('cardnumber')
        cvv = request.POST.get('cvv')
        exp = request.POST.get('exp')
        print(name)
        print(cardnumber)
        print(cvv)
        print(exp)
        car = cards.objects.all()
        '''for i in car:
            print(i.name)
            print(i.cardnumber)
            print(i.cvv)
            print(i.expdate)'''
        if (name == 'ARYA AJI' and cardnumber == '1234 5678 9012 3456') and (cvv == '329' and exp == '05 / 24'):
                """print('name:',i.name)
                print(name)
                print('name:',i.cardnumber)
                print(cardnumber)
                print('name:',i.cvv)
                print('name:',cvv)
                print('name:',i.expdate)
                print('name:',exp)"""
                proid = request.POST.get('proid')
                item = products.objects.get(id=proid)
                remain = item.stock
                item.stock = remain-1
                item.save()
                lastorder = orders.objects.last()
                lastorder.cstatus = 'Order Accepted'
                lastorder.save()
                lastorder = orders.objects.last()
                log = customers.objects.last()
                email = log.email
                subject = 'Order Details'
                m = ' Your Order Details '
                n = lastorder.customer
                o = 'Delivery Address:\t'+lastorder.caddress
                p = str(lastorder.ctime)+','+str(lastorder.cdate)
                q = 'Total amount paid:\t'+str(lastorder.camount)+' /- Rs'
                messagedupe = m+'\n\n'+'Dear\t'+n+','+'\n'+o+'\nDelivery Time & Date\t'+p+'\n'+q
                print(messagedupe)
                message = messagedupe
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'paymentmsg.html',{'msg':'Payment Success!!!!'})
        else:
                last = orders.objects.last()
                last.delete()
                return render(request,'paymentmsg.html',{'msg':'Payment Failed!!!!'})