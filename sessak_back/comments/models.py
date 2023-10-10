from django.db import models


# Create your models here.
class Comment(models.Model):
    comment = models.TextField(verbose_name="댓글")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="댓글 작성시간")

    author = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="댓글 작성자",
    )
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="post_comments",
        null=True,
        verbose_name="해당 게시물",
    )

    def __str__(self) -> str:
        return f"{self.author} - {self.comment} / {self.post}"
