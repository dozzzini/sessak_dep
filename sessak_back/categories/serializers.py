from rest_framework.serializers import ModelSerializer
from .models import Category
from rest_framework import serializers


class CategorySerializer(ModelSerializer):
    pass

    class Meta:
        model = Category
        fields = ["name"]
