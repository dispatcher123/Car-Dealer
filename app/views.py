
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest
from app.forms import CarForm
from django.shortcuts import get_object_or_404, redirect, render
from account.models import CustomUser
from account.forms import RegistrationForm
from django.db.models import Count
# Create your models here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from .models import CarModel,Car
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from .filters import CarFilter
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, message
from datetime import datetime,timedelta
from django.urls import reverse
from django.contrib import messages
import stripe
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.template import loader
##################### REGISTER , LOGIN , LOGOUT ####################


def register(request):
    if request.method=="POST":
        forms=RegistrationForm(request.POST)
        if forms.is_valid():
            email=forms.cleaned_data['email']
            first_name=forms.cleaned_data['first_name']
            last_name=forms.cleaned_data['last_name']
            password=forms.cleaned_data['password']
            confirm_password=forms.cleaned_data['confirm_password']
            username=email.split('@')[0]

            user=CustomUser.objects.create_user(email=email,first_name=first_name,last_name=last_name,username=username,password=password)
            user.save()
            current_site=get_current_site(request)
            mail_subject='Please active your account'
            message=render_to_string('verification.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email= EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect("/login/?command=verification&email="+email)

    else:
        forms=RegistrationForm()

    return render(request, 'register.html',context={
        'forms' : forms
    })


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def user_login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
            
        else:
            messages.error(request,'Invalid Login!')
            return redirect('register')
    
    return render(request, 'login.html',context={})



@login_required(login_url='/')
def user_logout(request):
    auth.logout(request)
    return redirect('login')
    
    
    


def home(request):
    cars=Car.objects.all().order_by('-id')
    forms=CarFilter(request.GET,queryset=cars)
    cars=forms.qs      
    paginator=Paginator(cars,9)
    page=request.GET.get('page')
    paginate_product=paginator.get_page(page)
    
    return render(request, 'home.html',context={
        'cars' : paginate_product,
        'forms' :forms
       
    })


def car_detail(request,slug):
    car=Car.objects.get(slug=slug)
    car.views = car.views +1
    car.save()
    return render(request, 'car_detail.html',context={
        'car' : car
    })
    


@login_required
def userpage(request):
    return render(request, 'user_page.html', context={})

@login_required
def dashboard(request):
    # total message 
    total=[]
    cong=25
    user=CustomUser.objects.get(id=request.user.id)
    queryset = Car.objects.filter(user=user)
    for a in queryset:
        total.append(a.views)
    views=sum(int(t) for t in total)
    paginator=Paginator(queryset, 5)
    total_adversite=queryset.count()
    
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    if views == cong :
        current_site=get_current_site(request)
        mail_subject='Auto'
        message=render_to_string('information.html', {
                'user': user,
                'domain': current_site,
                'views' : views
            })
        to_email=user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
    print(views)
    return render(request, 'index.html', context={
        'user' : user,
        'views' : views,
        'total_adversite' : total_adversite,
        'queryset' : queryset,
        'paged_products' : paged_products
    })





@login_required
def car_form(request):
    
    form=CarForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        send=form.save(commit=False)
        send.user=request.user
        send.save()
        
        return redirect('home')
                
    else:
        form=CarForm(request.POST)
    return render(request, 'car_form.html',context={
        'form': form
    })
    
stripe.api_key='sk_test_51JAExNCbKiyyexfdkXljLo7D1ujo55kqJngYWQkIbybPoqkM8O4Eo3F7ktiC67qrsnI5YStCWAokPfbN7YXlOPZa00T0UOKmav' #Pls write here your stripe secret keys

@login_required
def form(request):
    form=CarForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        send=form.save(commit=False)
        send.user=request.user
        
        send.save()
        return redirect(reverse('payment'))
                
    else:
        form=CarForm(request.POST)
    return render(request, 'form.html',context={
        'form': form
    })
    
@login_required
def payment(request):
    if request.method == "POST":
        membership= request.POST.get('membership','MONHTLY')
        amount = 10
        if membership == "YEARLY":
            amount = 100

        customer=stripe.Customer.create(
            email=request.user.email,
            source=request.POST['stripeToken']

        )
        charge=stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='usd',
            description= "Membership"
        )
        if charge['paid']==True:
            p=Car.objects.filter(user=request.user,is_avilable=False).latest('id')
            if charge['amount'] == 1000:
                p.subscription = "M"
                p.is_avilable=True
                expiry=datetime.now() + timedelta(30)
                p.expiry_date =expiry
                p.save()
            elif charge['amount'] == 10000:
                p.subscription = "Y"
                p.is_avilable=True
                expiry= datetime.now()+timedelta(365)
                p.expiry_date=expiry
                p.save()
                print(p)
            return redirect('success')

    return render(request, 'paid.html', context={})
@login_required
def success(request):
    return render(request, 'charge.html',context={})
    
    

########### MESSAGE

from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Message


from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

@login_required
def Inbox(request):
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
        
		}

	template = loader.get_template('direct.html')

	return HttpResponse(template.render(context, request))

@login_required
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('search_user.html')
	
	return HttpResponse(template.render(context, request))



    

@login_required
def Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct':active_direct,
        'message' : message
	}

	template = loader.get_template('direct.html')

	return HttpResponse(template.render(context, request))


@login_required
def NewConversation(request, username):
    
	from_user = request.user
	body = 'Hello!'
	try:
		to_user = CustomUser.objects.get(username=username)
	except Exception as e:
		return redirect('home')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('inbox')
    


@login_required
def SendDirect(request):
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	if request.method == 'POST':
		to_user = CustomUser.objects.get(username=to_user_username)
        
		Message.send_message(from_user, to_user, body)
        
		return redirect('inbox')
        
	else:
		HttpResponseBadRequest()

def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}

