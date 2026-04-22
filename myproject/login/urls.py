from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('profile/delete', views.delete_profile, name='delete_profile'),
    path('saves', views.saves, name='saves'),
    path('saves/update/<int:page>', views.saves_update, name='saves_update'),
    path('saves/delete/<get_id>', views.saves_delete, name='saves_delete'),
    path('topics/update/<page>', views.topic_update, name='topic_update'),
    path('topics/delete/<topic_id>', views.topic_delete, name='topic_delete'),
    path('password-reset', PasswordResetView.as_view(template_name="login/password_reset_form.html",
                                                            email_template_name="login/password_reset_email.html"),
                                                            name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(template_name="login/password_reset_done.html"),
                                                            name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="login/password_reset_confirm.html"),
                                                            name='password_reset_confirm'),
    path('password-reset/complete', PasswordResetCompleteView.as_view(template_name="login/password_reset_complete.html"),
                                                            name='password_reset_complete'),
    path('test-view', views.TestView.as_view(), name='test_view'),
]