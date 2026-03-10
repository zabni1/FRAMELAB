from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('profile<full_name>', views.profile, name='profile'),
    path('profile/update', views.update_profile, name='update_profile'),
]