from rest_framework import serializers
from .models import User, Query, Source, Result

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first', 'last')

class QuerySerializer(serializers.ModelSerializer):
    # keywords foreign key -> query primary key
    keywords = serializers.StringRelatedField(many=True)
    # user foreign key -> username field
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Query
        fields = ('id', 'name', 'description', 'user', 'keywords')

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'text', 'url', 'sourceType')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('run_id', 'source_id')