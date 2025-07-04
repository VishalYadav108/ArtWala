from rest_framework import serializers
from .models import Forum, ForumPost, ForumComment, PostLike, ForumMembership
from users.serializers import UserSerializer

class ForumSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Forum
        fields = '__all__'
    
    def get_posts_count(self, obj):
        return obj.posts.count()

class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    forum_name = serializers.CharField(source='forum.name', read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ForumPost
        fields = '__all__'
    
    def get_comments_count(self, obj):
        return obj.comments.count()

class ForumCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = ForumComment
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = PostLike
        fields = '__all__'

class ForumMembershipSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    forum_details = ForumSerializer(source='forum', read_only=True)
    
    class Meta:
        model = ForumMembership
        fields = '__all__'
        read_only_fields = ['joined_at']
