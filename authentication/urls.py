from django.urls import path
from .views import RegisterView,VerifyEmail,LoginView,RequestPasswordResetEmail,PasswordTokenCheckAPI,SetNewPasswordAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('email-verify/',VerifyEmail.as_view(),name='email-verify'),
    path('login/',LoginView.as_view(),name='login'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),


    path('password/reset/',RequestPasswordResetEmail.as_view(),name='request-password-reset'),
    path('password/reset/confirm/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(),name='password-reset-confirm'),
    path('password/reset/complete/',SetNewPasswordAPIView.as_view(),name='password-reset-complete'),




]

