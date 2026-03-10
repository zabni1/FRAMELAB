from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView

from .forms import LoginForm, RegisterForm, ProfileUserForm


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request)
                return redirect('home')
    return render(request, '', {'form': form})


def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, '',{'form': form})

def logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request, full_name):
    model = User.objects.get(full_name=full_name)
    return render(request, '', {'model': model})


@login_required(login_url='login')
def update_profile(request):
    form = ProfileUserForm(instance=request.user)
    return render(request, '', {'form': form})
