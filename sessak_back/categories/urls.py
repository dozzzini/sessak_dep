from django.urls import path
from . import views

urlpatterns = [
    path("newcategory/", views.NewCategory.as_view()),
    path("categorylist/", views.CategoryList.as_view()),
    path("<int:pk>/", views.CategoryDetails.as_view()),
]
