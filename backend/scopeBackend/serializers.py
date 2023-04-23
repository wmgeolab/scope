from rest_framework import serializers
from .models import User, Query, Source, Result, Run, SourceType, KeyWord, Workspace

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first', 'last')

# class KeywordSerializer(serializers.StringRelatedField):
#     def to_internal_value(self, data):
#         return KeyWord(word=data)
class KeywordSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return str(instance)
    
    def to_internal_value(self, data):
        return {'word': data}

    class Meta:
        model = KeyWord
        fields = ('word',)

class QuerySerializer(serializers.ModelSerializer):
    # keywords foreign key -> query primary key
    # keywords = serializers.StringRelatedField(many=True)
    keywords = KeywordSerializer(many=True, read_only=False)
    # keywords = serializers.ListField(
    #     # child=KeywordSerializer(many=True)
    # )
    # user foreign key -> username field
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    def create(self, validated_data):
        # print(validated_data)
        kws = validated_data['keywords']
        print(kws)
        q = Query.objects.create(
            user=validated_data['user'],
            name=validated_data['name'],
            description=validated_data['description']
        )
        for kw in kws:
            KeyWord.objects.create(query=q, word=kw['word'])
        return q

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

class WorkspaceSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Workspace
        fields = ('id', 'name', 'owner', 'user', 'tags', 'sources', 'password', 'status')

class WorkspaceMembersSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    workspace = WorkspaceSerializer()

    class Meta:
        model = Result
        fields = ('id', 'user', 'workspace')

class WorkspaceEntriesSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer()
    source = SourceSerializer()

    class Meta:
        model = Result
        fields = ('id', 'workspace', 'source')