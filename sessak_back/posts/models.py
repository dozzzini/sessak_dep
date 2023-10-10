from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="게시글 제목")
    content = models.TextField(verbose_name="게시글 내용")
    image = models.ImageField(upload_to="", null=True, blank=True, verbose_name="첨부파일")
    # like_num = models.PositiveIntegerField(default=0, verbose_name="좋아요 수")
    like_users = models.ManyToManyField(
        "users.User",
        blank=True,
        related_name="like_posts",
        verbose_name="좋아요 누른 사람",
    )
    # comment_num = models.PositiveIntegerField(default=0, verbose_name="댓글 수")
    view_num = models.PositiveIntegerField(
        default=0,
        verbose_name="조회수",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="게시글 작성날짜",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="게시글 수정날짜",
    )

    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="게시글 작성자",
    )

    category = models.ForeignKey(
        "categories.Category",
        max_length=10,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="카테고리",
    )

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"


# class Like(models.Model):
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     post = models.ForeignKey("posts.Post", on_delete=models.CASCADE)
