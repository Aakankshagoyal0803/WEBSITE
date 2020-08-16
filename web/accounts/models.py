from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class customer(models.Model):
    #one to one realtionship with django model User
    #blank true means we can create a customer without any user attached to it
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True,unique=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    profile_pic=models.ImageField(default='empty.jpg' ,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name


class tag(models.Model):
    name=models.CharField(max_length=200,null=True)

class product(models.Model):
    CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			)

    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    tags = models.ManyToManyField(tag)
    #enables admin user to select more than one tag associated with a product
    def __str__(self):
        return self.name
#http://127.0.0.1:8000/customer/1/?customer=&product=&date_created=&status=Pending#

class order(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
            #foreign key is one to many realtionship from customer to order
    customer=models.ForeignKey(customer,null=True,on_delete=models.SET_NULL)
    #shows drop down list of all the registered customer
    product=models.ForeignKey(product,null=True,on_delete=models.SET_NULL)
    #show drop down list of all the available products we havw
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=200,choices=STATUS)
    note=models.CharField(max_length=2000,null=True)
    def __str__(self):
        return self.product.name
