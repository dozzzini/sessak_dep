from django.contrib import admin
from .models import Post


# Register your models here.
@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category"]
    list_display_links = ["title"]
