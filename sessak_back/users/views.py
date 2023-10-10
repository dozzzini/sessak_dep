from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken
from .serializers import UserSerializer, SignupSerializer
from .models import User
from posts.serializers import PostListSerializer
from comments.serializers import CommentSerializer

# Create your views here.


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:  # 사용자가 인증되었는지 확인
            user = request.user
            serializer = UserSerializer(user)
            return Response(
                {
                    "data": serializer.data,
                    "post": PostListSerializer(
                        user.post_set.all(),
                        # Post.objects.filter(pk = request.user.pk)
                        many=True,
                    ).data,
                    "comment": CommentSerializer(
                        user.comment_set.all(),
                        many=True,
                    ).data,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"detail": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

    def put(self, request):
        if request.user.is_authenticated:
            user = request.user
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"detail": "인증되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED
            )


class SignUp(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            print(request.data)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return Response(
                {
                    # "user": serializer.data,
                    "message": "회원가입에 성공했습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
