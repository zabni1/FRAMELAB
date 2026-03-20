from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('profile/delete', views.delete_profile, name='delete_profile'),
    path('saves', views.saves, name='saves'),
    path('saves/update/<int:page>', views.saves_update, name='saves_update'),
    path('saves/delete/<get_id>', views.saves_delete, name='saves_delete'),
    path('topics', views.topic_users, name='topics'),
    path('topics/update', views.topic_update, name='topic_update'),
    path('topics/delete/<topic_id>', views.topic_delete, name='topic_delete'),
]