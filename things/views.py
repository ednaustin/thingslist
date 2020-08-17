from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ThingsForm
from .models import Things
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
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

@login_required
def currentthings(request):
    newthings = Things.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'things/currentthings.html', {'things':newthings})

@login_required
def completedthings(request):
    newthings = Things.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'things/completedthings.html', {'things':newthings})

@login_required
def viewthing(request, thing_pk):
    thing = get_object_or_404(Things, pk=thing_pk, user=request.user)
    if request.method == 'GET':
        form = ThingsForm(instance=thing)
        return render(request, 'things/viewthing.html', {'thing':thing, 'form':form})
    else:
        try:
            form = ThingsForm(request.POST, instance=thing)
            form.save()
            return redirect('currentthings')
        except ValueError:
            return render(request, 'things/viewthing.html', {'thing':thing, 'form':form, 'error':'Bad info. Try again.'})

@login_required
def completething(request, thing_pk):
    thing = get_object_or_404(Things, pk=thing_pk, user=request.user)
    if request.method == 'POST':
        thing.datecompleted = timezone.now()
        thing.save()
        return redirect('currentthings')

@login_required
def deletething(request, thing_pk):
    thing = get_object_or_404(Things, pk=thing_pk, user=request.user)
    if request.method == 'POST':
        thing.delete()
        return redirect('currentthings')
