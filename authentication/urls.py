from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('check_mail/', views.check_mail, name="check_mail"),
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name="authentication/reset_password.html"),
         name="reset_password"),
    path('password/reset/sent/', auth_views.PasswordResetDoneView.as_view(template_name="authentication/reset_password_done.html"),
         name="password_reset_done"),
    path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/reset_password_confirm.html"),
         name="password_reset_confirm"),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="authentication/reset_password_complete.html"),
         name="password_reset_complete"),
    path('password/change/', auth_views.PasswordChangeView.as_view(template_name="authentication/change_password.html"),
         name="password_change"),
    path('password/change/complete/',
         auth_views.PasswordChangeDoneView.as_view(template_name="authentication/change_password_complete.html"), name="password_change_done"),
    path('password/set/', auth_views.PasswordResetView.as_view(
        template_name="authentication/set_password.html"), name="set_password"),
]
