from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count, Sum

# Restframework에서 불러온 것들
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
    NotFound,
    PermissionDenied,
    ParseError,
)
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

# paginator를 위해 불러올 것들
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# 모델 불러오기
from .models import Post
from comments.models import Comment

# serializers 불러오기
from .serializers import (
    PostSerializer,
    PopularPostSerializer,
)
from comments.serializers import CommentSerializer

# 검색기능에 사용할 Q 불러오기
from django.db.models import Q


# 새 게시글 작성 API
class NewPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_post = serializer.save(author=request.user)
        return Response(
            PostSerializer(new_post).data,
            status=status.HTTP_201_CREATED,
        )


# 모든 게시글 조회
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def all_post(request):
    # 전체 포스트가 담겨 있는 객체들을 생성일 최신순으로 정렬 + 위치 정보
    try:
        user = request.user
        post_list = Post.objects.filter(author__location=user.location).order_by(
            "-created_at"
        )
    except:
        return Response(
            {"message": "위치 정보를 확인해주세요."}, status=status.HTTP_401_UNAUTHORIZED
        )

    #'page'라는 명으로 들어온 값을 가져오기
    page = int(request.GET.get("page", 1))

    paginator = Paginator(post_list, 7)

    try:
        # 페이지마다 할당된 포스팅이 담겨있는 객체
        page_obj = paginator.page(page)

        # 페이지 숫자에 아무것도 들어오지 않을 경우 1페이지로 인식
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)

    except EmptyPage:
        # 존재하지 않는 page를 입력할 때 1페이지로 이동
        # page = paginator.num_pages
        # page = 1
        # page_obj = paginator.page(page)
        raise NotFound("존재하지 않는 페이지입니다.")

    leftIndex = int(page) - 2
    if leftIndex < 1:  # 현재 페이지가 1일 경우 마이너스가 되지 않도록 최솟값을 1로 설정
        leftIndex = 1

    rightIndex = int(page) + 2
    if (
        rightIndex > paginator.num_pages
    ):  # 현재 페이지가 마지막 페이지(=내가 가지고 있는 마지막 페이지)를 넘을 수 없도록 최댓값을 마지막 페이지로 설정
        rightIndex = paginator.num_pages

    # 페이지 수를 고정
    while rightIndex - leftIndex + 1 >= 5:
        leftIndex += 1

    total_page = list(range(leftIndex, rightIndex + 1))
    page_list = PostSerializer(page_obj, many=True).data

    return Response(
        {
            "total_page": total_page,
            "page_list": page_list,
        },
        status=status.HTTP_200_OK,
    )


# 각 게시글 조회, 수정 , 삭제 API
class PostDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            post = self.get_object(pk)
            post.view_num = post.view_num + 1
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except post.DoesNotExist:
            return Response(
                {"message": "게시글을 찾을 수 없습니다"}, status=status.HTTP_404_NOT_FOUND
            )

    # def get(self, request, pk):
    #     try:
    #         post = self.get_object(pk)
    #         comment = Comment.objects.filter(post__pk=pk)
    #         post.view_num = post.view_num + 1
    #         post.save()
    #         serializer = PostSerializer(post)
    #         return Response(
    #             {
    #                 "post_data": serializer.data,
    #                 "comment_data": CommentSerializer(
    #                     comment,
    #                     many=True,
    #                 ).data,
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     except post.DoesNotExist:
    #         return Response(
    #             {"message": "게시글을 찾을 수 없습니다"}, status=status.HTTP_404_NOT_FOUND
    #         )

    def put(self, request, pk):
        post = self.get_object(pk)
        print("해당 게시글:", post)
        serializer = PostSerializer(
            post,
            data=request.data,
            # partial=True,
        )
        # print("serializer_1: ", serializer)
        if post.author != request.user:
            raise PermissionDenied("수정권한이 없습니다")

        if serializer.is_valid():
            updated_post = serializer.save()
            return Response(
                {
                    "message": "게시글이 수정되었습니다.",
                    "data": PostSerializer(updated_post).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        post = self.get_object(pk)

        if post.author != request.user:
            raise PermissionDenied("삭제권한이 없습니다")

        post.delete()

        return Response(
            {"message": "게시글이 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )


# 좋아요 추가 및 취소
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise NotFound("해당 게시물이 없습니다.")

    if post.like_users.filter(pk=request.user.pk).exists():
        # 넌 취소를 할 수 있어
        post.like_users.remove(request.user.pk)
        print("좋아요취소")
        return Response(status=status.HTTP_200_OK)
    else:
        # 만약 안 들어와있어
        post.like_users.add(request.user.pk)
        # 그럼 누를 수 있어
        return Response(status=status.HTTP_200_OK)


# 게시물 검색 - 제목 또는 내용
class PostSearch(APIView):
    def get(self, request):
        keyword = request.GET.get("keyword", "")  # 검색어

        if keyword:
            results = Post.objects.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )
        else:
            results = Post.objects.none()

        serializer = PostSerializer(results, many=True)
        return Response(serializer.data)


# 인기게시물 정렬
@api_view(["GET"])
def popular_posts_view(request):
    popular_posts = Post.objects.annotate(
        total_nums=Count("like_users") + Sum("view_num") + Count("post_comments")
    ).order_by("-total_nums")[:10]

    serializer = PopularPostSerializer(popular_posts, many=True)
    return Response({"popular_posts": serializer.data})
