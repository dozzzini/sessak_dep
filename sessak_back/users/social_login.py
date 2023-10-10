from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import ValidationError, BadRequest
from users.models import User
from django.contrib.auth import login
import os, environ

# from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from rest_framework.decorators import api_view
import requests
from rest_framework import status
import logging
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response

# from rest_framework.renderers import JSONRenderer
from . import serializers

# state = getattr(settings, "STATE")
logger = logging.getLogger(__name__)

state = "random_string"
# BASE_URL = "http://127.0.0.1:8000/"
# BASE_URL = "https://port-0-sessak-back2-cgw1f2almhig6l2.sel5.cloudtype.app/"
# GOOGLE_CALLBACK_URI = BASE_URL + "api/v1/users/google/callback/"
GOOGLE_CALLBACK_URI = "https://port-0-sessak-back2-cgw1f2almhig6l2.sel5.cloudtype.app/api/v1/users/google/callback/"


@api_view(["GET"])
def google_login(request):
    """
    Code Request
    """

    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"

    client_id = settings.GOOGLE_AUTH_CLIENT_ID
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


@api_view(["GET"])
def google_callback(request):
    client_id = settings.GOOGLE_AUTH_CLIENT_ID
    client_secret = settings.GOOGLE_AUTH_SECRET
    code = request.GET.get("code")
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise ValidationError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    profile_req_status = profile_req.status_code
    if profile_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    profile_req_json = profile_req.json()
    print(profile_req_json)
    data = {
        "email": profile_req_json.get("email"),
        "name": profile_req_json.get("name", ""),
        "image": profile_req_json.get("picture", None),
    }

    try:
        user = User.objects.get(email=data["email"])
    except User.DoesNotExist:
        user = None
    if user is not None:
        if user.login_method != User.LOGIN_GOOGLE:
            raise BadRequest("잘못된 요청입니다.")
    else:
        user = User(
            email=data["email"],
            login_method=User.LOGIN_GOOGLE,
        )
        user.set_unusable_password()  # 우리 딴에서는 패워가 더 이상 필요하지 않으니까
        user.save()

    token = TokenObtainPairSerializer.get_token(user)
    refresh_token = str(token)
    access_token = str(token.access_token)

    res = Response(
        {
            "user": serializers.UserSerializer(user).data,
            "message": "로그인 성공",
            "token": {
                "access": access_token,
                "refresh": refresh_token,
            },
        },
        status=status.HTTP_200_OK,
    )

    res.set_cookie("access", access_token, httponly=True)
    res.set_cookie("refresh", refresh_token, httponly=True)
    login(
        request,
        user,
        backend="django.contrib.auth.backends.ModelBackend",
    )

    #
    return res


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


# @api_view(["GET"])
# def kakao_login(request):
#     client_id = os.environ.get("KAKAO_ID")
#     REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code"
#     )

# def kako_callback(request):
#     try:
#         code = request.GET.get("code")
#         client_id = os.environ.get("KAKAO_ID")
#         REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback"
#         token_request = requests.get(
#             f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={REDIRECT_URI}&code={code}"
#         )
