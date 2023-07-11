from django.shortcuts import render,redirect
from .models import Thread,ChatMessage
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        chatlists = Thread.objects.all()

        context = {
            "chatlists":chatlists
        }
        return render(request, 'index.html',context)
    else:
        return redirect('login')


def room(request, room_name):
    chatlists = Thread.objects.all()
    try:
        thread = Thread.objects.get(threadname = room_name)
        chatmessages = ChatMessage.objects.filter(thread = thread)
     
        context = {
            'room_name': room_name,
            "chatlists":chatlists,
            "chatmessages":chatmessages
        }
        return render(request, 'room.html', context)
    except:
    
        return redirect('home')
    