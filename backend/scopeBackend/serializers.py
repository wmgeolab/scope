from rest_framework import serializers
from .models import User, Query, Source, Result, Run, SourceType, KeyWord, Workspace, WorkspaceMembers, WorkspaceEntries, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first', 'last')

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
    keywords = KeywordSerializer(many=True, read_only=False)
    # user foreign key -> username field
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    def create(self, validated_data):
        # print(validated_data)
        kws = validated_data['keywords']
        # print(kws)
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
        fields = ('name', 'description')

class SourceSerializer(serializers.ModelSerializer):
    sourceType = SourceTypeSerializer()

    class Meta:
        model = Source
        fields = ('id', 'text', 'url', 'sourceType')

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ('query', 'time')

class ResultSerializer(serializers.ModelSerializer):
    # run foreign key -> query primary key
    run = RunSerializer()
    # source foreign key -> result primary key
    source = SourceSerializer()

    class Meta:
        model = Result
        fields = ('id', 'run', 'source')

class TagSerializer(serializers.ModelSerializer):
    def to_string(self, instance):
        return str(instance)
    
    def to_internal_value(self, data):
        return {'tag': data}
    
    class Meta:
        # do not remove the comma
        # needed for django to recognize that this is a tuple with only one object
        # reference: https://stackoverflow.com/questions/36264728/django-error-the-fields-option-must-be-a-list-or-tuple-or-all
        model = Tag
        fields =('tag',)

class WorkspaceSerializer(serializers.ModelSerializer):
    # refer to QuerySerializer for example
    tags = TagSerializer(many=True, read_only=False)
    creatorId = serializers.SlugRelatedField(read_only=True, slug_field='id')

    def create(self, validated_data):
        # create workspace
        # unique name defined in models
        w = Workspace.objects.create(
            name=validated_data['name'],
            password=validated_data['password'],
            creatorId=validated_data['creatorId']
        )
        # add creator to workspace
        WorkspaceMembers.objects.create(
            member=w.creatorId,
            workspace=w
        )
        # add tags
        tags = validated_data['tags']
        for t in tags:
            Tag.objects.create(workspace=w, tag=t['tag'])
        return w

    class Meta:
        model = Workspace
        fields = ('id', 'name', 'tags', 'password', 'creatorId')

class WorkspaceMembersSerializer(serializers.ModelSerializer):
    member = serializers.SlugRelatedField(read_only=True, slug_field='id')
    workspace = WorkspaceSerializer()

    def create(self, validated_data):
        # add member to workspace
        m = WorkspaceMembers.objects.create(
            member=validated_data['member'],
            workspace=validated_data['workspace']
        )
        return m

    class Meta:
        model = WorkspaceMembers
        fields = ('member', 'workspace')

class WorkspaceEntriesSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer()
    source = SourceSerializer()

    def create(self, validated_data):
        # add source to workspace
        e = WorkspaceEntries.objects.create(
            workspace=validated_data['workspace'],
            source=validated_data['source']
        )
        return e

    class Meta:
        model = WorkspaceEntries
        fields = ('workspace', 'source')
