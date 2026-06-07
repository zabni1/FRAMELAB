from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('<slug:show_cat>', views.CategoryPageView.as_view(), name='category'),
    path('update/<slug:show_cat>', views.UpdateSavedView.as_view(), name='update_saved'),
    path('translate/', views.TranslatePageView.as_view(), name='translate'),
    path('detail/<slug:show_more>', views.DetailPageView.as_view(), name='detail'),
    path('error_404/', views.error_view, name='error_404'),
    path('error_500/', views.error_500_view, name='error_500'),
]