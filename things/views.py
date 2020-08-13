from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ThingsForm
from .models import Things

def home(request):
    return render(request, 'things/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'things/signupuser.html', {'form':UserCreationForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentthings')
            except IntegrityError:
                return render(request, 'things/signupuser.html', {'form':UserCreationForm(), 'error':"That username has already been taken. Please enter a new username."})
        else:
            return render(request, 'things/signupuser.html', {'form':UserCreationForm(), 'error':"Passwords did not match"})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'things/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'things/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and or password did not match'})
        else:
            login(request, user)
            return redirect('currentthings')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def createthings(request):
    if request.method == 'GET':
        return render(request, 'things/createthings.html', {'form':ThingsForm()})
    else:
        try:
            form = ThingsForm(request.POST)
            newthing = form.save(commit=False)
            newthing.user = request.user
            newthing.save()
            return redirect('currentthings')
        except ValueError:
            return render(request, 'things/createthings.html', {'form':ThingsForm(), 'error':'Bad data passed in. Try again.'})

def currentthings(request):
    newthings = Things.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'things/currentthings.html', {'things':newthings})
