from rest_framework import serializers
from .models import Article, Newsletter
from users.serializers import UserSerializer
from publications.serializers import PublisherSerializer

class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.
    Includes nested serialization for author and publisher details.
    """
    author = UserSerializer(read_only=True)
    publisher_detail = PublisherSerializer(source='publisher', read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'created_at', 'updated_at', 'approved', 'author', 'publisher', 'publisher_detail', 'approved_by']
        read_only_fields = ['author', 'approved_by', 'approved', 'created_at', 'updated_at']

class NewsletterSerializer(serializers.ModelSerializer):
    """
    Serializer for the Newsletter model.
    """
    author = UserSerializer(read_only=True)
    articles = ArticleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Newsletter
        fields = ['id', 'title', 'description', 'created_at', 'author', 'articles']
        read_only_fields = ['author', 'created_at']
