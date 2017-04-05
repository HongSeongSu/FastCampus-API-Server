from rest_framework import serializers

from member.serializers import UserSerializer
from post.models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'pk',
            'post',
            'img',
            'created_date',
        )
        read_only_fields = ('post', )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    images = PostImageSerializer(source='postimage_set', many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'images',
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

        files = self.context['request'].FILES.getlist('images')
        for file in files:
            PostImage.objects.create(
                post=post,
                img=file
            )
        return post
