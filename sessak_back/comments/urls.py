from django.urls import path
from . import views

urlpatterns = [
    path("newcomment/", views.NewComment.as_view()),
    path("<int:comment_id>/", views.CommentDetails.as_view()),
]
