from typing import Callable

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


def check_is_request_user_author(func: Callable):
    def wrapper(self, request, *args, **kwargs):
        # каждый раз обращаться к бд - не очень оптимизированно,
        # наверное, но лучшего решения как-то не придумал...
        if request.user != self.get_object().author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return func(self, request, *args, **kwargs)

    return wrapper


class CommentSerializer(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(post=post, author=post.author)

    @check_is_request_user_author
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @check_is_request_user_author
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GroupView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @check_is_request_user_author
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @check_is_request_user_author
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
