from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView
from .forms import LoginForm, RegisterForm, ProfileUserForm
from main.email_services import send_email_after_login, send_email_after_registration
from main.models import Saved
from topic.models import Topic


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request)
                send_email_after_login(email)
                return redirect('home')
    return render(request, 'login/login.html', {'form': form})


def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_email_after_registration(user.email)
            return redirect('home')
    return render(request, 'login/signup.html',{'form': form})

def logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request):
    # model = User.objects.get(full_name=request.user.full_name)
    photo = settings.DEFAULT_USER_IMAGE
    saved = Saved.objects.filter(email=request.user.email)
    return render(request, 'login/profile.html', {'model': '', 'photo': photo, 'saved': saved})


@login_required(login_url='login')
def update_profile(request):
    form = ProfileUserForm(instance=request.user)
    photo = settings.DEFAULT_USER_IMAGE
    return render(request, 'login/update_profile', {'form': form, 'photo': photo})

@login_required(login_url='login')
def delete_profile(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return redirect('home')


@login_required(login_url='login')
def saves(request):
    page = 9
    saved = Saved.objects.filter(email=request.user.email).select_related('detail')
    return render(request, 'login/saves.html', {'saved': saved})

@login_required(login_url='login')
def saves_update(request):
    return None

@login_required(login_url='login')
def saves_delete(request, get_id):
    if request.headers.get('HX-Request'):
        delete = Saved.objects.get(id=get_id)
        delete.delete()
        saved = Saved.objects.filter(email=request.user.email).select_related('detail')
        return render(request, 'partials/saves_delete.html', {'saved': saved})
    return redirect('login')

@login_required(login_url='login')
def topic_users(request):
    topic = Topic.objects.filter(email=request.user.email)
    return render(request, 'login/topics.html', {'topic': topic})

@login_required(login_url='login')
def topic_update(request):
    return None

@login_required(login_url='login')
def topic_delete(request, topic_id):
    if request.headers.get('HX-Request'):
        delete = Saved.objects.get(id=topic_id)
        delete.delete()
        topic = Topic.objects.filter(email=request.user.email)
        return render(request, 'login/topics.html', {'topic': topic})
    return redirect('login')






