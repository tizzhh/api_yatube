from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class IsAuthRequestUserOwnerOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthRequestUserOwnerOrReadOnly,)

    def get_queryset(self):
        return self.get_post_obj(self.kwargs.get('post_pk')).comments.all()

    def perform_create(self, serializer):
        post = self.get_post_obj(self.kwargs.get('post_pk'))
        serializer.save(post=post, author=post.author)

    @staticmethod
    def get_post_obj(pk: int):
        return get_object_or_404(Post, pk=pk)


class GroupView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthRequestUserOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
