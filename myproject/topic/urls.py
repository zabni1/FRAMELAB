from django.urls import path
from . import views

urlpatterns = [
    path('', views.TopicPageView.as_view(), name='topic'),
    path('update/<int:page>', views.TopicUpdatePageView.as_view(), name='topic_update_page'),
    path('detail/<slug:show_detail>', views.TopicDetailView.as_view(), name='topic_detail'),
    path('create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('update/<int:pk>', views.TopicUpdateView.as_view(), name='topic_update'),
    path('delete/<int:pk>', views.TopicDeleteView.as_view(), name='topic_delete'),
    path('update-comments/<int:pk>', views.create_comment, name='create_comment'),
    path('delete-comments/<int:pk>', views.delete_comment, name='delete_comments'),
    path('get-input-for_reply/<int:pk>', views.get_input_for_reply, name='get_input_for_reply'),
    path('get-input-for-reply-on-reply/<int:pk>/<str:username>', views.get_input_for_reply_on_reply,
                                                                       name='get_input_for_reply_on_reply'),
    path('create-reply/<int:pk>', views.create_reply, name='create_reply'),
    path('create_reply_on_reply/<int:pk>/<str:username>', views.create_reply_on_reply, name='create_reply_on_reply'),
    path('delete-reply/<int:pk>', views.delete_reply, name='delete_reply'),
    path('get-reply/<int:pk>', views.get_replies, name='get_replies'),
]