from django.urls import path
from . import views

urlpatterns = [
    path('', views.TopicPageView.as_view(), name='topic'),
    path('update/<int:page>', views.TopicUpdatePageView.as_view(), name='topic_update_page'),
    path('detail/<show_detail>', views.TopicDetailView.as_view(), name='topic_detail'),
    path('create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('update/<slug:slug>', views.TopicUpdateView.as_view(), name='topic_update'),
    path('delete/<slug:slug>', views.TopicDeleteView.as_view(), name='topic_delete'),
]