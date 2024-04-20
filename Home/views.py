from django.shortcuts import render,  redirect,HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . models import product,Gallery,customer,cart,Feedback,faqsection,Payment,Orders
from . forms import customerProfileForm
import re
import razorpay
from uuid import uuid4


def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(email_pattern, email):
        return True
    else:
        return False

def homepage(request):
    """  Product=product.objects.filter()
    Title=product.objects.filter().values('title')
    Price=product.objects.filter().values('selling_price') """
    return render(request,'index.html',locals())

def services(request):
    return render(request,'serv.html')

class shop(View):
    def get(self,request):
        Product=product.objects.filter()
        Title=product.objects.filter().values('title')
        Price=product.objects.filter().values('selling_price')
        return render(request,'shop.html',locals())

class product_details(View):
    def get(self,request,pk):
        Product = product.objects.get(id=pk)
        return render(request,'product_details.html',locals())

@login_required
def orders(request):
    order_placed = Orders.objects.filter(user=request.user)
    return render(request,'orders.html',locals())

def accountPage(request):
    if request.method=='POST':
        if 'register' in request.POST:
            uname=request.POST.get('logname')
            uemail=request.POST.get('logemail')
            upass=request.POST.get('logpass')
            if not uname.isalpha():
                return HttpResponse('<script>alert("Name must only alphabets")</script>')
            if len(uname) < 8:
                return HttpResponse('<script>alert("Name must greater than 8 characters")</script>')
            if not validate_email(uemail):
               return HttpResponse('<script>alert("Email is not valid")</script>')
            if len(upass) < 8:
                return HttpResponse('<script>alert("Password must greater than 8 characters")</script>')
            new_user= User.objects.create_user(uname,uemail,upass)
            new_user.save()
        elif 'login' in request.POST:
            name = request.POST.get('logname')
            passw = request.POST.get('logpass')
            user = authenticate(request,username=name,password=passw)
            if user is not None:
                login(request,user)
                return redirect('/')
    return render(request,'login.html')

@method_decorator(login_required,name='dispatch')
class profileView(View):
    def get(self,request):
        form = customerProfileForm()
        return render(request,'profile.html',locals())
    def post(self,request):
       form= customerProfileForm(request.POST)
       if form.is_valid():
           user =request.user
           name = form.cleaned_data['name']
           address = form.cleaned_data['address']
           mobile = form.cleaned_data['mobile']
           zipcode = form.cleaned_data['zipcode']
           state = form.cleaned_data['state']

           reg= customer(user=user,name=name,address=address,mobile=mobile,zipcode=zipcode,state=state)
           reg.save()
           messages.success(request,"Profile saved successfully")
       else:
           messages.warning(request,"Invalid input data")
       return render(request,'profile.html',locals())

@login_required
def address(request):
    add = customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = customer.objects.get(pk=pk)
        form = customerProfileForm(instance=add)
        return render(request,'updateAddress.html',locals())
    def post(self,request,pk):
        form = customerProfileForm(request.POST)
        if form.is_valid():
            add = customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.address = form.cleaned_data['address']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Profile Updated')
        else:
            messages.warning(request,'Invalid input data')
        return redirect("Home:address")

@method_decorator(login_required,name='dispatch')
class deleteAddress(View):
    def get(self,request,pk):
        add = customer.objects.get(pk=pk)
        add.delete()
        return redirect("Home:address")

@login_required    
def addtocart(request):
    user = request.user
    product_id = request.GET.get('prod-id') 
    print(product_id)
    Product = product.objects.get(id=product_id)
    cart(user=user,product=Product).save()
    return redirect('Home:showcart')

def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity +=1
        c.save()
        user = request.user
        Cart = cart.objects.filter(user=user)
        amount=0
        for i in Cart:
            value = i.quantity * i.product.selling_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -=1
        c.save()
        user = request.user
        Cart = cart.objects.filter(user=user)
        amount=0
        for i in Cart:
            value = i.quantity * i.product.selling_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def removecart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user = request.user
        Cart = cart.objects.filter(user=user)
        amount=0
        for i in Cart:
            value = i.quantity * i.product.selling_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        user = request.user
        add= customer.objects.filter(user=user)
        cart_items = cart.objects.filter(user=user)
        amount=0
        for i in cart_items:
            value = i.quantity * i.product.selling_price
            amount = amount + value
        totalamount = amount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency":"INR","receipt":"order_rcptid_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
      #  {'id': 'order_MgF9nNqiNjbrJK', 'entity': 'order', 'amount': 66100, 'amount_paid': 0, 'amount_due': 66100, 'currency': 'INR', 'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1695573969}
        order_id = payment_response["id"]
        order_status = payment_response["status"]
        if order_status == "created":
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request,'checkout.html',locals())

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id'),
    payment_id = request.GET.get('payment_id'),
    cust_id = request.GET.get('cust_id'),
    #print("payment_done : oid = ",order_id," pip = ",payment_id," cid = ",cust_id[0])
    user = request.user
    #return redirect("Home:orders")
    Customer = customer.objects.get(id=cust_id[0])
    payment = Payment.objects.get(razorpay_order_id = order_id[0])
    payment.paid = True
    payment.razorpay_payment_id = payment_id[0]
    payment.save()
    Cart = cart.objects.filter(user=user)
    for c in Cart:
        Orders(user=user,customer=Customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("Home:orders") 

@login_required
def showcart(request):
    user = request.user
    Cart = cart.objects.filter(user=user)
    amount=0
    for i in Cart:
        value = i.quantity * i.product.selling_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'addtocart.html',locals())

def about(request):
    return render(request,'About.html')

class gallery(View):
    def get(self,request):
        gallery=Gallery.objects.filter()
        return render(request,'gallery.html',locals())

def contact(request):
    return render(request,'contact.html')
def faq(request):   
    faqs = faqsection.objects.filter()
    return render(request,'faq.html',locals())

def cctv(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/CCTV.html',locals())

def bio(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/bio.html',locals())

def assemble(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/assemble.html',locals())

def LED(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter() 
    return render(request,'services/led.html',locals())

def LEDboard(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage')
    feedbacks = Feedback.objects.filter() 
    return render(request,'services/ledboard.html',locals())

def count(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/count.html',locals())

def bill(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/bill.html',locals())


def paper(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/paper.html',locals())

def barcode(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage')
    feedbacks = Feedback.objects.filter()
    return render(request,'services/barcode.html',locals())

def restaurant(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/restaurant.html',locals())

def textiles(request): 
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage')
    feedbacks = Feedback.objects.filter()
    return render(request,'services/textiles.html',locals())

def supermarket(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/supermarket.html',locals())

def agency(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/agency.html',locals())

def accounting(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/accounting.html',locals())

def webdesign(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/webdesign.html',locals())

def hosting(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/hosting.html',locals())

def domin(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/domin.html',locals())

def server(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/server.html',locals())

def mobile(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/mobile.html',locals())

def bulksms(request):
    if request.method == 'POST':
        content = request.POST.get('feedback')
        print(content)
        
        if request.user.is_authenticated:
            feedback = Feedback(user=request.user, content=content)
            feedback.save()
        else:
            return redirect('Home:accountPage') 
    feedbacks = Feedback.objects.filter()
    return render(request,'services/bulksms.html',locals())


def tpay(request): 
    amount = 1000
    return render(request,'tpay.html',locals())
def initiate_payment(request):
    url = "https://test.cashfree.com/api/v1/order/create"
    payload = {
        "appId" : "TEST10025071d437f319b2bffe62a13117052001",
        "secretKey":"TESTb4eb72476569ee49ed56709ae6415197c19a6b99",
        "orderId":f"order_{uuid4()}",
        "orderAmount":"1000",
        "orderCurrency":"INR",
        "orderNote":"Thankyou fro purchasing from VS Services",
        "customerName":"Dummy",
        "customerEmail":"Dummy@123.com",
        "customerPhone":"9576832985",
        "returnUrl":"",
        "notifyUrl":""
    }
    responce = requests.request("POST",url,data=payload)
    text = responce.text
    data_dict = json.loads(text)

    if data_dict["status"] == "OK":
        return redirect(data_dict["paymentLink"])
    else:
        return JsonResponse({"error":"Payment Unsuccessfull"})