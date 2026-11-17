from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("dang-ky/", views.register, name="register"),
    path("dang-nhap/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("dang-xuat/", auth_views.LogoutView.as_view(), name="logout"),
]
