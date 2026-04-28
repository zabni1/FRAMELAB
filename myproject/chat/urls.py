from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat, name='chat'),
    path('get-messages/<int:page>', views.get_messages, name='get_messages'),
    path('add-message', views.add_message, name='add_message'),
    path('get-messages/<str:message>', views.get_message, name='get_message'),
    path('clear-chat', views.clear_chat, name='clear_chat'),
]