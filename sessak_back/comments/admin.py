from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class UserAdmin(admin.ModelAdmin):
    list_display = ["comment", "author", "post"]
    list_display_links = ["comment"]
