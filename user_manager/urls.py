"""Urls of User_Manager"""
from django.urls import path # pylint: disable=R0801

from . import views # pylint: disable=R0801

urlpatterns = [
    path('registration/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),

    path('password-reset-sent/<str:reset_id>/',
                views.password_reset_sent_view, name='password-reset-sent'),

    path('reset-password/<str:reset_id>/', views.reset_password_view, name='reset-password'),
]
