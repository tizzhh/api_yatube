from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Comment, Group, Post


# Сори, я забыл смержить ветки xD
class IsRequestUserOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return request.user == obj.author


class CommentSerializer(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsRequestUserOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(post=post, author=post.author)


class GroupView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsRequestUserOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
