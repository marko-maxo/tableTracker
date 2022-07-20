from django.urls import path
from .views import *
from rest_framework import routers


urlpatterns = [
    path('login/', LoginUserView.as_view(), name="loginView"),
    path('logout/', LogoutView.as_view(), name="logoutView"),
    path('user_info/', UserInfo.as_view(), name="user_info"),
    path('admin_info/', UserInfoOnlyAdmin.as_view(), name="admin_info"),
]
