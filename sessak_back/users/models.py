from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random, string
from django.contrib.auth.models import PermissionsMixin
from django.utils.crypto import get_random_string


# Create your models here.
class UserManager(BaseUserManager):
    """
    User 모델 관리 클래스
    """

    use_in_migrations = True  # 마이그레이션에 UserManager에 포함하는 코드

    def create_user(
        self,
        email,
        password,
        nickname,
        profile_image,
        name,
        **kwargs,
    ):
        if not email:
            raise ValueError("이메일은 필수사항입니다.")
        user = self.model(
            email=email,
            nickname=nickname,
            profile_image=profile_image,
            name=name,
        )
        user.set_password(password)  # 패스워드 해시 암호화
        user.save(using=self._db)  # 기본 User 모델을 이용하여 저장하는 코드
        return user

    def create_superuser(
        self,
        email,
        nickname,
        name="admin",
        profile_image=None,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("이메일은 필수사항입니다.")
        user = self.create_user(
            email=email,
            nickname=nickname,
            password=password,
            profile_image=profile_image,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)  # 기본 User 모델을 이용하여 저장하는 코드
        return user


def generate_random_string():
    return "".join(random.choice(string.ascii_letters) for _ in range(5))


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nickname = models.CharField(
        max_length=5,
        default=generate_random_string,
        unique=True,
    )
    location = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    profile_image = models.URLField(null=True)
    username = models.CharField(max_length=10, blank=True, null=True)

    LOGIN_HOME = "home "
    LOGIN_GOOGLE = "google"
    LOGIN_CHOICES = (
        (LOGIN_HOME, "home"),
        (LOGIN_GOOGLE, "google"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "location"]

    login_method = models.CharField(
        max_length=8, choices=LOGIN_CHOICES, default=LOGIN_HOME
    )

    def __str__(self) -> str:
        return f"{self.nickname} ({self.location})"

    objects = UserManager()

    class Meta:
        db_table = "user"
