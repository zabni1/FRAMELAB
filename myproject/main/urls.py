from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('list/<slug:show_cat>', views.CategoryPageView.as_view(), name='category'),
    path('update/<int:page>/<slug:show_cat>', views.UpdateCategoryPageView.as_view(), name='update_cat'),
    path('detail/<slug:show_more>', views.DetailPageView.as_view(), name='detail'),
    path('about', views.AboutPageView.as_view(), name='about'),
    path('response', views.ChatView.as_view(), name='response'),
    path('error', views.error_view, name='error'),
]