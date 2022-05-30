from asyncio.windows_events import NULL
from hashlib import new
import json
from django.contrib import messages
from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import resolve

 
from chat.models import Thread, ChatMessage
from .forms import CustomRegisterForm



################  below this line all views functions not required user logged in  ##################


def index(request):
    if request.user.is_authenticated: 
        return redirect('chat/')
    else:
        return render(request, 'auth.html') 

def user_register(request): 
    if request.user.is_authenticated: 
        return redirect('chat/')
    else:
        form = CustomRegisterForm() 
        if request.method == 'POST':
            form = CustomRegisterForm(request.POST)
            if form.is_valid(): 
                form.save() 
                
                # auto login after register  
                username = request.POST.get('username')
                password = request.POST.get('password1')
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    print('logged in :- ', user)
                    return redirect('chat/')
            else:
                context = {}
                messages.error(request, 'error')
                return redirect('/auth', context)
                
        context = {
            'form': form
        }
        return render(request, 'auth.html', context)
    
def user_login(request):
    if request.user.is_authenticated: 
        return redirect('chat/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('logged in :- ', user)
                return redirect('chat/')
            else:
                context = {}
                messages.error(request, 'Username or Password is incorrect')
                return redirect('/auth', context)
        
        context = {}
        return render(request, 'auth.html', context)

 
################  above this line all views functions not required user logged in  ##################
#
#
#
#
################# below this line all views required user logged in #################################


#---# fetching data from database and displaying on chat page #---#
@login_required(login_url='/auth')
def messages_page(request):
    # users = User.objects.values()
    # print('user ::-- ', users)
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    all_threads = Thread.objects.all()
    context = {
        'Threads': threads,
        'all_threads': all_threads
        # 'users': users
    } 
    print(threads)
    return render(request, 'messages.html', context)

@login_required(login_url='/auth')
def user_logout(request):
    logout(request)
    return redirect('/')
 
 
#---# searching query handles this function #---#
@login_required(login_url='/auth')
def search_users(request): 
    user = ''
    query = request.POST['query']
    if len(query): 
        user = User.objects.filter(username__icontains=query) 
        
    else: 
        user = {}
        print('else is print :: ', request)
    
    # Convert the QuerySet to a List
    list_of_dicts = list(user.values())
     
    # Convert List of Dicts to JSON
    res = json.dumps(list_of_dicts, indent=4, sort_keys=True, default=str)
 
    return HttpResponse(res, content_type="application/json") 

#---# creating new thread for first time after user clicking on "Say, Hi" button #---#
@login_required(login_url='/auth')
def create_new_thread(request):
    
    httpResponse = ''
    
    if request.method == 'POST': 
        first_person =  User.objects.get(id=request.POST.get('user_id'))
        second_person =  User.objects.get(id=request.POST.get('receiver_id'))
        global multiple_query
        multiple_query = Q(Q(first_person=first_person) & Q(second_person=second_person))
        
        if Thread.objects.filter(multiple_query).exists():
            print('yes')
            existing_thread_id = Thread.objects.get(multiple_query) 

            # inserting first message "hi" into the existing created thread
            inserting_message = ChatMessage.objects.create(thread=existing_thread_id, user=first_person, message='Hi, this is auto generated, and repeated.')

            httpResponse = 'thread_exist_and_send_message'

        else:
            print('no')
            # creating new thread for two users
            new_thread_id = Thread.objects.create(first_person=first_person, second_person=second_person, is_first_msg=True, first_sender=first_person)
            
            # inserting first message "hi" into the newly created thread
            ChatMessage.objects.create(thread=new_thread_id, user=first_person, message='Hi !')
        
            httpResponse = 'new_thread_created_and_send_message'   
 
    else:
        httpResponse = 'this_method_is_not_POST'
        
    
    res = Thread.objects.filter(multiple_query)
    # res = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    list_of_dicts = list(res.values())
    
    # Convert List of Dicts to JSON
    res = json.dumps(list_of_dicts, indent=4, sort_keys=True, default=str)
 
    httpResponse = {
        'res': res,
        'httpResp': httpResponse,
    }
    return HttpResponse(res, content_type="application/json") 


#---# checking that user has first msg true or not #---#
@login_required(login_url='/auth')
def check_first_msg(request):
    
    httpResponse = ''
    
    if request.method == 'POST':
        httpResponse = Thread.objects.filter(id=request.POST.get('active_thread_id')) 
    else:
        httpResponse = 'request_not_valid'

    list_of_dicts = list(httpResponse.values())
    
    # Convert List of Dicts to JSON
    httpResponse = json.dumps(list_of_dicts, indent=4, sort_keys=True, default=str)
 
    return HttpResponse(httpResponse)


#---# updating the status of first message  #---#
@login_required(login_url='/auth')
def update_first_status(request):
    httpResponse = ''
    
    if request.method == 'POST':
        httpResponse = Thread.objects.filter(id=request.POST.get('active_thread_id')).update(is_first_msg=False)
        httpResponse = 'status_updated'
    else:
        httpResponse = 'request_not_valid'
    
    
    print(httpResponse)
    
    return HttpResponse(httpResponse)

