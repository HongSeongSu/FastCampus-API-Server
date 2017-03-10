from rest_framework import serializers

from member.serializers import UserSerializer
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'title',
            'img_cover',
            'content'
        )
        read_only_fields = ('author', )

    def create(self, validated_data):
        post = Post(
            author=self.context['request'].user,
            title=validated_data['title'],
            img_cover=validated_data.get('img_cover', None),
            content=validated_data.get('content', '')
        )
        post.save()
        return post
