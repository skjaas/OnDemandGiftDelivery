from django.db import models

# Create your models here.

class customers(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    class Meta:
        db_table = "customers"


class sellers(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=6)
    class Meta:
        db_table = "sellers"

class login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    verified = models.CharField(max_length=20)
    class Meta:
        db_table = "login"

class products(models.Model):
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    idealfor = models.CharField(max_length=20)
    stock = models.IntegerField()
    sellerId = models.IntegerField()
    image = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    class Meta:
        db_table = "products"

class sellerlogin(models.Model):
    sellerid = models.IntegerField()
    class Meta:
        db_table = "sellerlogin"

class customerlogin(models.Model):
    customerid = models.IntegerField()
    class Meta:
        db_table = "customerlogin"

class orders(models.Model):
    customer = models.CharField(max_length=50)
    citemname = models.CharField(max_length=20)
    cdate = models.DateField(null=True)
    ctime = models.TimeField(null=True)
    camount = models.IntegerField()
    caddress = models.CharField(max_length=500)
    cstatus = models.CharField(max_length=20)
    csellerid = models.IntegerField()
    cproductid = models.IntegerField()
    cid = models.IntegerField()
    cimage = models.CharField(max_length=100)
    class Meta:
        db_table = "orders"

class cards(models.Model):
    name = models.CharField(max_length=50)
    cardnumber = models.CharField(max_length=19)
    cvv = models.IntegerField()
    expdate = models.CharField(max_length=7)
    class Meta:
        db_table = "cards"
