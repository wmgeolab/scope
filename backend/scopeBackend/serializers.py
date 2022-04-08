from rest_framework import serializers
from .models import User, Query, Source, Result, Run, SourceType

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

class SourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceType
        fields = ( 'name', 'description')

class SourceSerializer(serializers.ModelSerializer):
    sourceType = SourceTypeSerializer()
    class Meta:
        model = Source
        fields = ('id', 'text', 'url', 'sourceType')

class RunSerializer(serializers.ModelSerializer):
    query = QuerySerializer()
    class Meta:
        model = Run
        fields = ('query', 'time')

class ResultSerializer(serializers.ModelSerializer): 
    # run = RunSerializer()
    # source = SourceSerializer(many=True)
    # run foreign key -> query primary key 
    # source = serializers.StringRelatedField(read_only=True)
    source = SourceSerializer()
    run = RunSerializer()
    # result foreign key -> run primary key
    # run = serializers.PrimaryKeyRelatedField(read_only=True)
    # source foreign key -> result primary key
    # source = serializers.PrimaryKeyRelatedField(many = True, read_only=True)
    # source = serializers.StringRelatedField(many = True, read_only=True)

    class Meta:
        model = Result
        fields = ('id', 'run', 'source')