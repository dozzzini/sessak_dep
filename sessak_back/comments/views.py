from django.shortcuts import render

# Restframework에서 불러온 것들
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.response import Response

# 모델 불러오기
from .models import Comment
from posts.models import Post

# serializers 불러오기
from .serializers import CommentSerializer, UpdatedCommentSerializer


# 새 댓글 작성 API (해당 게시물에 대한)
class NewComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        try:
            post = Post.objects.get(id=request.data.get("post_id"))
        except Post.DoesNotExist:
            raise NotFound("해당하는 게시글이 없습니다")

        if serializer.is_valid():
            new_comment = serializer.save(author=request.user, post=post)
            return Response(
                CommentSerializer(new_comment).data,
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {"message": "내용을 입력하세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 댓글 수정, 삭제 API
class CommentDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_post(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound("게시글이 존재하지 않습니다.")

    def get_comment(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            raise NotFound("댓글이 존재하지 않습니다.")

    # def get(self, request, post_id):
    #     post = self.get_post(post_id)
    #     print("조회:", post)
    #     comments = post.post_comments.all()
    #     print("댓글:", comments)

    def put(self, request, comment_id):
        comment = self.get_comment(comment_id)
        print("댓글:", comment)
        serializer = CommentSerializer(
            comment,
            data=request.data,
            # partial=True,
        )
        if comment.author != request.user:
            raise PermissionDenied("수정권한이 없습니다")

        if serializer.is_valid():
            updated_comment = serializer.save()
            return Response(
                {
                    "message": "댓글이 수정되었습니다.",
                    "data": UpdatedCommentSerializer(updated_comment).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, comment_id):
        comment = self.get_comment(comment_id)

        if comment.author != request.user:
            raise PermissionDenied("삭제권한이 없습니다")

        comment.delete()

        return Response(
            {"message": "댓글이 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )
