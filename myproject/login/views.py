from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.template.response import TemplateResponse
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


def signup(request):
    token_generator = default_token_generator
    form = RegisterForm(request.POST)
    if request.headers.get('HX-Request'):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
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
            return TemplateResponse(request, 'login/signup_complete.html', context)
        else:
            return TemplateResponse(request, 'login/signup_error.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'login/signup.html',{'form': form})


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
        user = get_object_or_404(get_user_model(),username=username, active_status=True)
        topics = Topic.objects.filter(
            email=request.user.email)
        return render(request, 'login/user_profile.html', {'user': user, 'topics': topics,
                                                                                'page': page,'photo': photo})
    else:
        user = get_object_or_404(get_user_model(), username=username, active_status=True)
        topics = Topic.objects.filter(
            email=request.user.email)
    return render(request, 'login/profile.html', {'user': user, 'topics': topics,
                                                                       'page': page, 'photo': photo})


@login_required(login_url='login')
def update_profile(request, username):
    get_user = get_user_model().objects.get(username=username)
    photo = settings.DEFAULT_USER_IMAGE
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('profile', username=user.username)
    else:
        form = ProfileUserForm(instance=request.user)
    return render(request, 'login/update_profile.html', {'form': form, 'photo': photo, 'user': get_user})

@login_required(login_url='login')
def delete_profile(request, username):
    user = get_user_model().objects.get(username=username)
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
            return render(request, 'partials/topic_user_update_last.html', {
                'topics': topics
            })
        else:
            return render(request, 'partials/topic_user_update.html', {
                'topics': topics,
                'page': page + 9
            })
    return redirect('login')

@login_required(login_url='login')
def topic_delete(request, topic_id):
    if request.headers.get('HX-Request'):
        delete = Topic.objects.get(id=topic_id)
        delete.delete()
        topics = Topic.objects.filter(email=request.user.email)
        return render(request, 'partials/topic_user_update.html', {'topics': topics[:9],
                                                                                        'page': 9})
    return redirect('login')

@login_required(login_url='login')
def saves(request):
    page = 0
    saved = Saved.objects.filter(email=request.user.email)
    context = {
        'saved': saved,
        'page': page,
    }
    return render(request, 'login/saves.html', context)

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
        return render(request, 'partials/saves_update.html', {'saved': saved[:9], 'page': 9})
    return redirect('login')








