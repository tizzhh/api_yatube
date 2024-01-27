from typing import Callable

from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import PostSerializer
from posts.models import Comment, Group, Post


def check_is_author(func: Callable):
    def wrapper(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return func(self, request, *args, **kwargs)

    return wrapper


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @check_is_author
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @check_is_author
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
