from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # list_display = ["email", "nickname", "location"]
    # list_display_links = ["nickname"]
    # fieldsets = (
    #     (
    #         ("회원정보"),
    #         {
    #             "fields": (
    #                 "email",
    #                 "nickname",
    #                 "location",
    #             ),
    #         },
    #     ),
    # )
    list_display = ("__str__",)
