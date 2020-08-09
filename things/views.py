from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login

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

def currentthings(request):
    return render(request, 'things/currentthings.html')
