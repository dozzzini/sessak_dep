from django.urls import path
from . import views

urlpatterns = [
    path("newpost/", views.NewPost.as_view()),
    path("postlist/", views.all_post),
    path("<int:pk>/", views.PostDetails.as_view()),
    path("like/<int:pk>/", views.like_post),
    path("popular_post/", views.popular_posts_view),
    path("post_search/", views.PostSearch.as_view()),
]
