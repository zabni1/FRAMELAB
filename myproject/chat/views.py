from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .chat_services import get_request, get_reply
from .models import Message


@login_required(login_url='login')
def chat(request):
    messages = Message.objects.filter(Q(user1=request.user.pk,user2=0) |
                                     Q(user1=0,user2=request.user.pk)).order_by('pk')
    page = messages.count()

    context = {
            'messages': messages,
            'page': page,
        }
    return render(request, 'chat/main.html', context)


@login_required(login_url='login')
def get_messages(request, page):
    if request.headers.get('HX-Request'):
        messages = Message.objects.filter(Q(user1=request.user.pk, user2=0) |
                                          Q(user1=0, user2=request.user.pk)).order_by('pk')
        start = page - 5
        end = page

        if start <= 0:
            return render(request, 'chat/get_messages_last.html', {'messages': messages[0:end]})
        else:
            return render(request, 'chat/get_messages.html', {'messages': messages[start:end],
                                                                                   'page': int(start)})
    return redirect('chat')


@login_required(login_url='login')
def add_message(request):
    if request.headers.get('HX-Request'):
        message = request.POST.get('message')
        context = get_request(request.user.pk, message)
        return render(request, 'chat/add_message.html', context)
    return redirect('chat')


@login_required(login_url='login')
def get_message(request, message):
    if request.headers.get('HX-Request'):
        context = get_reply(request.user.pk, message)
        return render(request, 'chat/get_reply.html', context)
    return redirect('chat')


@login_required(login_url='login')
def clear_chat(request):
    if request.headers.get('HX-Request'):
        Message.objects.filter(Q(user1=request.user.pk, user2=0) |
                                          Q(user1=0, user2=request.user.pk)).order_by('pk').delete()
        return render(request, 'chat/clear_chat.html')
    return redirect('chat')

