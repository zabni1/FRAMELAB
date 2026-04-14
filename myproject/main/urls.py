from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('list/<slug:show_cat>', views.CategoryPageView.as_view(), name='category'),
    path('update/<slug:show_cat>', views.UpdateSavedView.as_view(), name='update_saved'),
    path('translate', views.TranslatePageView.as_view(), name='translate'),
    path('detail/<slug:show_more>', views.DetailPageView.as_view(), name='detail'),
    path('about', views.AboutPageView.as_view(), name='about'),
    path('test', views.test_view, name='test'),
    path('save_test/<int:key>', views.save_test, name='save_test'),
    path('error', views.error_view, name='error'),
]