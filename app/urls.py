from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('userpage/',userpage,name='userpage'),
    path('register/',register,name='register'),
    path('login/',user_login,name='login'),
    path('logout',user_logout,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    path('car-detail/<slug:slug>/',car_detail,name='car_detail'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('car_form/',car_form,name='car_form'),
    path('form/',form,name='form'),
    path('payment/',payment,name='payment'),
    path('success/',success,name='success'),
    path('inbox/', Inbox, name='inbox'),
   	path('directs/<username>/', Directs, name='directs'),
   	path('new/', UserSearch, name='usersearch'),
   	path('new/<username>/', NewConversation, name='newconversation'),
   	path('send/', SendDirect, name='send_direct'),
    
]
