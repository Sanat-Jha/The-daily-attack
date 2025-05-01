from rest_framework import serializers
from .models import Post, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'status', 'created_at', 'published_at', 'author', 'tags']

class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'tags']
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        
        # Add tags
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip().lower())
            post.tags.add(tag)
        
        return post