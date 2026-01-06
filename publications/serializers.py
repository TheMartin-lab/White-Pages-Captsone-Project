from rest_framework import serializers
from .models import Publisher
from users.serializers import UserSerializer

class PublisherSerializer(serializers.ModelSerializer):
    editors = UserSerializer(many=True, read_only=True)
    journalists = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Publisher
        fields = '__all__'
