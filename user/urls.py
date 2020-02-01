from django.urls import path

from .views import LoginView, LogoutView, RegisterView, ChangePasswordView

app_name = 'user'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    path('password/change', ChangePasswordView.as_view(), name='change password'),
]
