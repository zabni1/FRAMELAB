from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView, FormView
from .forms import ProfileForm, RegisterForm, ProfileUserForm
from .email_services import send_email_after_login, send_email_after_registration
from main.models import Saved
from topic.models import Topic
from .models import User


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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            send_email_after_registration(user.email)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'login/signup.html',{'form': form})

# class SingUpView(PasswordContextMixin, FormView):
#     template_name = 'login/signup.html'
#     success_url = reverse_lazy('password_reset_done')
#     form_class = RegisterForm
#     email_template_name = "login/password_reset_email.html"
#     token_generator = default_token_generator


class TestView(PasswordContextMixin, FormView):
        template_name = 'login/signup.html'
        success_url = reverse_lazy('password_reset_done')
        form_class = PasswordResetForm
        email_template_name = "login/password_reset_email.html"
        token_generator = default_token_generator
        title = "Password reset"
        extra_email_context = None
        from_email = None
        html_email_template_name = None
        subject_template_name = "registration/password_reset_subject.txt"


        @method_decorator(csrf_protect)
        def dispatch(self, *args, **kwargs):
            return super().dispatch(*args, **kwargs)

        def form_valid(self, form):
            opts = {
                "use_https": self.request.is_secure(),
                "token_generator": self.token_generator,
                "from_email": self.from_email,
                "email_template_name": self.email_template_name,
                "subject_template_name": self.subject_template_name,
                "request": self.request,
                "html_email_template_name": self.html_email_template_name,
                "extra_email_context": self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request, username):
    photo = settings.DEFAULT_USER_IMAGE
    page = 0
    if request.user.username == username:
        user = get_user_model().objects.get(username=username)
        saved = Saved.objects.filter(email=request.user.email)
        return render(request, 'login/user_profile.html', {'user': user, 'saved': saved,
                                                                                'page': page,'photo': photo})
    else:
        user = get_user_model().objects.get(username=username)
        saved = Saved.objects.filter(email=user.email)
    return render(request, 'login/profile.html', {'user': user, 'saved': saved,
                                                                       'page': page, 'photo': photo})


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
        ).select_related('detail')
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








