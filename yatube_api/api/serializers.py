from rest_framework import serializers

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # Явное лучше неявного!!!
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')
        optional_fields = ('image', 'group')
        read_only_fields = ('author', 'pub_date')
