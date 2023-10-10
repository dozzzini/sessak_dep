from django.urls import path
from . import views, social_login
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path(
        "userinfo/",
        views.UserInfo.as_view(),
        name="user-update",
    ),
    path(
        "google/login/",
        social_login.google_login,
        name="google_login",
    ),
    path(
        "google/callback/",
        social_login.google_callback,
        name="google_callback",
    ),
    path(
        "google/login/finish/",
        social_login.GoogleLogin.as_view(),
        name="google_login_todjango",
    ),
    path(
        "signup/",
        views.SignUp.as_view(),
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
    ),
    path(
        "refresh/",
        TokenRefreshView.as_view(),
    ),
]
