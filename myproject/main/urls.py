from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('error', views.ErrorView, name='error'),
]