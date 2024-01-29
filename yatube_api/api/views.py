from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


def get_post_obj(pk: int):
    return get_object_or_404(Post, pk=pk)


class IsAuthRequestUserOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    # Пришлось переопределить еще этот метод, т.к он
    # вызывается для эндпоинтов без объекта по типу
    # posts/ || comments/.
    # Поэтому встает вопрос о том, что лучше:
    # один пермишн вот так или 2 пермишена (этот и
    # IsAuthenticated).
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author


class CommentSerializer(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthRequestUserOwnerOrReadOnly,)

    def get_queryset(self):
        return get_post_obj(self.kwargs.get('post_pk')).comments.all()

    def perform_create(self, serializer):
        post = get_post_obj(self.kwargs.get('post_pk'))
        serializer.save(post=post, author=post.author)


class GroupView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthRequestUserOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
