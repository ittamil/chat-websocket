from django.shortcuts import render, redirect
# from .models import User
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username = username, password = password)
        return redirect('login')
    else:
        return render(request,'registration/register.html') 

    return render(request,'registration/register.html') 