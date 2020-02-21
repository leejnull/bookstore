from django.urls import path
from user import views as user_api

urlpatterns = [
    path('login', user_api.login, name='login'),
    path('ping_login', user_api.ping_login, name='ping_login'),
    path('logout', user_api.logout, name='logout'),
    path('register', user_api.register, name="register"),
    path('get_user_info', user_api.get_user_info, name="get_user_info")
]
