from rest_framework import serializers
from .models import User, Query

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first', 'last')

class QuerySerializer(serializers.ModelSerializer):
    keywords = serializers.StringRelatedField(many=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Query
        fields = ('id', 'name', 'description', 'user', 'keywords')
    