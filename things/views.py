from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def signupuser(request):

    return render(request, 'things/signupuser.html', {'form':UserCreationForm()})
