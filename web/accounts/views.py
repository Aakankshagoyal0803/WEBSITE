from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import orderform,createuserform,customer_formacc,customerform
from django.urls import reverse
from .filters import orderfilter
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorator import unauth_user,allowed_user,admin_only
from django.contrib.auth.models import Group

@unauth_user
def registerpage(request):
    #if request.user.is_authenticated:
    #    return redirect('home')
    #else:
      form=createuserform()
      if request.method=='POST':
          form=createuserform(request.POST)
          if form.is_valid():
              user=form.save()
              username=form.cleaned_data.get('username')

              group=Group.objects.get(name='customer') #customer is name of one group in admin
              user.groups.add(group)

              customer.objects.create(
              user=user, #customer has user field
              name=user.username,
              )
              #signals part
              messages.success(request,'account was created successfully for' + username)
              #add message in html of login to display flash messages
              return redirect('login')
      context={ 'form':form}
      return render(request,'accounts/register.html',context)

@unauth_user
def loginpage(request):
    #viewfunc will be the login page in decorator
    #if request.user.is_authenticated:
    #    return redirect('home')
    #else:
     if request.method=='POST':
         username=request.POST.get('username')
         password=request.POST.get('password')

         user=authenticate(request,username=username,password=password)
         if user is not None:
            login(request,user)
            return redirect('/')
         else:
            messages.info(request,'username and password incorrect')
     context={}
     return render(request,'accounts/login.html',context)

def logoutuser(request):
    logout(request,)
    return redirect('login')

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def user_page_view(request):
    orders=request.user.customer.order_set.all()
    total_order=orders.count()
    deliver=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    context={
    'orders':orders,
    'deliver':deliver,
    'pending':pending,
    'total_order':total_order,
    }
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles='customer')
def accountsettings(request):
    customer=request.user.customer #give logged in user at any time
    form=customer_formacc(instance=customer)
    #to do something with formed data recieved
    if request.method=='POST':
            #reuest.FILES bec we are dealing with image files also
            form=customer_formacc(request.POST,request.FILES,instance=customer)
            if form.is_valid:
                form.save()
    context={
    'form': form
    }
    return render(request,'accounts/accountsettings.html',context)


#@allowed_user(allowed_roles=['admin','staff'])
#because this page functionality can be access ed by admin only
@login_required(login_url='login')
#@allowed_user(allowed_roles=['admin'])
@admin_only #can pass any no. of parameters in that list
def home(request):
    ord=order.objects.all() #used ony to get total orders
    cust=customer.objects.all().order_by('-date_created')
    total_customer=cust.count()
    total_order=ord.count()
    deliver=ord.filter(status='Delivered').count()
    pending=ord.filter(status='Pending').count()
    fiveorder=order.objects.all().order_by('date_created')[:5]
    context={
    'orders':fiveorder,
    'customers':cust,
    'total_customer':total_customer,
    'total_order':total_order,
    'deliver':deliver,
    'pending':pending,
    }
    return render(request,'accounts/base.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def products(request):
    p=product.objects.all()
    return render(request,'accounts/products.html',{'products':p})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def customer_view(request,pk):
    c=customer.objects.get(id=pk)
    o=c.order_set.all()
    order_count=o.count()
    myfilter=orderfilter(request.GET,queryset=o)
    o=myfilter.qs
    return render(request,'accounts/customer.html',{'customers':c,'order':o,'order_count':order_count,'myfilter':myfilter})
 # Create your views here.

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def createorder(request,pk):
    #create form class just like orderform
    orderformset=inlineformset_factory(customer,order,fields=('product','status'),extra=10)
    #form=orderform(initial={'customer':cust})
    #customer is parent model order is child and fields tuple conatin required field
    cust=customer.objects.get(id=pk)
    #form=orderform(initial={'customer':cust})
    #to autoifll customer name when not using fieldset  in form
    #order.objects.null() to not fill any entry on its own in formset
    formset=orderformset(queryset=order.objects.none(),instance=cust)
    if request.method== 'POST':
        #print(request.POST)
        formset=orderformset(request.POST,instance=cust)

        if formset.is_valid():
             formset.save()
             return redirect('/')

    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def updateorder(request,pk):
    ins=order.objects.get(id=pk)
    form=orderform(instance=ins)
    if request.method== 'POST':
        #print(request.POST)
        form=orderform(request.POST,instance=ins)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/update_order.html',context)


#made it myself not exist in dennis project
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def createcustomer(request):
    form=customerform()
    if request.method=='POST':
        form=customerform(request.POST)
        if form.is_valid():
          form.save()
          return redirect('/')
    context={'form':form}
    return render(request,'accounts/customer_form.html',context)
#made iit myslef
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def updatecustomer(request,pk):
    i=customer.objects.get(id=pk)
    form=customerform(instance=i)
    if request.method=='POST':
        form=customerform(request.POST,instance=i)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def deleteorder(request,pk):
    ins=order.objects.get(id=pk)
    if request.method=="POST":
        ins.delete()
        return redirect('/')
    context={'item':ins}
    return render(request,'accounts/delete.html',context)


#not working how to delete customer
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','staff'])
def deletecustomer(request,pk):
    i=customer.objects.get(id=pk)
    if request.method=="POST":
        i.delete()
        return redirect('/')
    context={'customer':i}
    return render(request,'accounts/delete_customerr.html',context)
#chnaged in view section of each customer earlier it was showing delete customer after update customerhowing place oredr their
