from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name="카테고리명",
    )
    description = models.TextField(verbose_name="카테고리 설명")

    def __str__(self) -> str:
        return f"{self.name}"
