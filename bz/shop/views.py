from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Orders,Orderupdate
from django.contrib.auth.models import User,auth    
from django.contrib import messages
from math import *
import json

# Create your views here.

def index(request):
    #products =Product.objects.all()
    #n= len(products)
    #nSlides = n //4 + ceil((n/4)-(n//4))
    #params = {'no_of_slides':nSlides,'range':range(1,nSlides),'product':products}
    #allProds = [[products, range(1, nSlides), nSlides],[products, range(1, nSlides), nSlides]]
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}

    return render(request, 'shop/index.html',params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.Product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": "" , 'prod' : prod}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)



def about(request):
    return render(request,'shop/about.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('uname','')
        password=request.POST.get('password','')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/shop')
        else:
            messages.info(request,'invalid information..')
            return redirect('/shop/login/')
    else:
       return render(request,'shop/login.html')

def logout(request):
    auth.logout(request)
    return redirect("/shop")

def Register(request):
    if request.method =="POST":
        first_name=request.POST.get('fname','')
        last_name=request.POST.get('lname','')
        username = request.POST.get('uname','')
        email = request.POST.get('email','')
        password1=request.POST.get('password1','')
        password2=request.POST.get('password2','')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username already taken")
                return redirect("/shop/register/")
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
                user.save();
                messages.info(request,"user created")
                return redirect('/shop/login/')
        else:
            messages.info(request,"password not matching..")
    return render(request,'shop/register.html')

def contact(request):
    if request.method =="POST":
        email = request.POST.get('email','')
        name=request.POST.get('name','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')

        ok = True
        contact = Contact(name=name,email=email, phone=phone,desc=desc)
        contact.save()
        return render(request,'shop/contact.html',{'ok':ok})
    return render(request,'shop/contact.html')





def tracker(request):
     if request.method =="POST":
        orderId =request.POST.get('orderId','')
        email = request.POST.get('email','')

        try:
            order = Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update = Orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc,'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

     return render(request,'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')


def productview(request, myid):
    # fetch the product using id
    product = Product.objects.filter(id=myid)

    return render(request,'shop/prodview.html',{'product':product[0]})


def checkout(request):
    if request.method =="POST":
        itemsJson = request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email = request.POST.get('email','')
        address =request.POST.get('address1','')+" "+ request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        order = Orders(items_json=itemsJson,name=name,email=email, address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        
        order.save()
        update = Orderupdate(order_id=order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request,'shop/checkout.html',{'thank':thank ,'id':id});
    return render(request,'shop/checkout.html')



