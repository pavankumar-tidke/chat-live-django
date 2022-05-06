from django.contrib import messages
from multiprocessing import context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from chat.models import Thread
from .forms import CustomRegisterForm

# Create your views here.

# @login_required

def user_register(request): 
    form = CustomRegisterForm()
    
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            print('register in :- ', form)
            form.save() 
            
            # auto login after register  
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)
             
            print('logged in 1 :- ', user)
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

def user_logout(request):
    logout(request)
    return redirect('/auth')






def index(request):
    return render(request, 'index.html')




@login_required(login_url='/auth')

def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)


