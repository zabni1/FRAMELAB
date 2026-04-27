from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, resolve_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import ProfileForm, RegisterForm, ProfileUserForm
from .email_services import confirm_email, send_email_after_login, send_email_after_registration
from main.models import Saved
from topic.models import Topic



def user_login(request):
    if request.method == 'POST':
        form = ProfileForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                send_email_after_login(user.email)
                return redirect('home')
    else:
        form = ProfileForm()
    return render(request, 'login/login.html', {'form': form})


def signup_confirm(request):
    token_generator = default_token_generator
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            domain = current_site.domain
            user_pk_bytes = force_bytes(user.pk)
            context = {
                'protocol': 'http',
                'domain': domain,
                'uid':urlsafe_base64_encode(user_pk_bytes),
                'token': token_generator.make_token(user),
                'username': user.username,
            }
            confirm_email(email=user.email, context=context)
            return redirect('signup_complete')
    else:
        form = RegisterForm()
    return render(request, 'login/signup.html',{'form': form})


def signup_complete(request):
    return render(request, 'login/signup_complete.html')


def signup_done(request, uidb64, token):
    uid =  urlsafe_base64_decode(uidb64).decode()
    user = get_user_model().objects.get(pk=uid)
    user.active_status = True
    user.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    send_email_after_registration(user.email)
    return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request, username):
    photo = settings.DEFAULT_USER_IMAGE
    page = 0
    if request.user.username == username:
        user = get_user_model().objects.get(username=username, active_status=True)
        topics = Topic.objects.filter(
            email=request.user.email)
        return render(request, 'login/user_profile.html', {'user': user, 'topics': topics,
                                                                                'page': page,'photo': photo})
    else:
        user = get_user_model().objects.get(username=username, active_status=True)
        topics = Topic.objects.filter(
            email=request.user.email)
    return render(request, 'login/profile.html', {'user': user, 'topics': topics,
                                                                       'page': page, 'photo': photo, })


@login_required(login_url='login')
def update_profile(request):
    form = ProfileUserForm(instance=request.user)
    photo = settings.DEFAULT_USER_IMAGE
    return render(request, 'login/update_profile', {'form': form, 'photo': photo})

@login_required(login_url='login')
def delete_profile(request):
    user = get_user_model().objects.get(id=request.user.id)
    user.delete()
    return redirect('home')


@login_required(login_url='login')
def topic_update(request, page):
    if request.headers.get('HX-Request'):
        topics_qs = Topic.objects.filter(
            email=request.user.email
        )
        topics = topics_qs[page:page + 9]

        if page + 9 >= topics_qs.count():
            return render(request, 'partials/saves_update_last.html', {
                'topics': topics
            })
        else:
            return render(request, 'partials/saves_update.html', {
                'topics': topics,
                'page': page + 9
            })
    return redirect('login')

@login_required(login_url='login')
def topic_delete(request, topic_id):
    if request.headers.get('HX-Request'):
        delete = Saved.objects.get(id=topic_id)
        delete.delete()
        topics = Topic.objects.filter(email=request.user.email)
        return render(request, 'login/topics.html', {'topics': topics})
    return redirect('login')

@login_required(login_url='login')
def saves(request):
    page = 0
    return render(request, 'login/saves.html', {'page': page})

@login_required(login_url='login')
def saves_update(request, page):
    if request.headers.get('HX-Request'):
        saved_qs = Saved.objects.filter(
            email=request.user.email
        ).select_related('detail')
        saved = saved_qs[page:page + 9]

        if page + 9 >= saved_qs.count():
            return render(request, 'partials/saves_update_last.html', {
                'saved': saved
            })
        else:
            return render(request, 'partials/saves_update.html', {
                'saved': saved,
                'page': page + 9
            })
    return redirect('login')


@login_required(login_url='login')
def saves_delete(request, get_id):
    if request.headers.get('HX-Request'):
        delete = Saved.objects.get(id=get_id)
        delete.delete()
        saved = Saved.objects.filter(email=request.user.email).select_related('detail')
        return render(request, 'partials/saves_delete.html', {'saved': saved})
    return redirect('login')








