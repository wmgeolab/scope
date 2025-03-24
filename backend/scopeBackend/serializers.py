from rest_framework import serializers
from .models import User, Query, Source, Result, Run, SourceType, KeyWord, Workspace, WorkspaceMembers, WorkspaceEntries, Tag, AiResponse, Revision, WorkspaceQuestions

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

class WorkspaceSerializer(serializers.ModelSerializer):
    # refer to QuerySerializer for example
    # tags = TagSerializer(many=True, read_only=False)
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
        return w

    class Meta:
        model = Workspace
        fields = ('id', 'name', 'password', 'creatorId')

class WorkspaceMembersSerializer(serializers.ModelSerializer):
    member = serializers.SlugRelatedField(read_only=True, slug_field='id')
    workspace = WorkspaceSerializer(read_only=True)
    workspace_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        # add member to workspace
        m = WorkspaceMembers.objects.create(
            member=validated_data['member'],
            workspace=validated_data['workspace']
        )
        return m

    class Meta:
        model = WorkspaceMembers
        fields = ('member', 'workspace', 'workspace_id')

class WorkspaceEntriesSerializer(serializers.ModelSerializer):
    workspace = serializers.IntegerField(write_only=True)
    source = SourceSerializer(read_only=True)
    source_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        # add source to workspace
        e = WorkspaceEntries.objects.create(
            workspace=validated_data['workspace'],
            source=validated_data['source']
        )
        return e

    class Meta:
        model = WorkspaceEntries
        fields = ('workspace', 'source', 'source_id')

class WorkspaceQuestionsSerializer(serializers.ModelSerializer):
    workspace_id = serializers.IntegerField(write_only=True)
    question = serializers.CharField()

    def create(self, validated_data):
        # add question to workspace
        e = WorkspaceQuestions.objects.create(
            question=validated_data['question'], 
            workspace_id=validated_data['workspace_id']
        )
        return e

    class Meta:
        model = WorkspaceQuestions
        fields = ('question', 'workspace_id')
    

class TagSerializer(serializers.ModelSerializer):
    workspace = serializers.IntegerField()

    def create(self, validated_data):
        t = Tag.objects.create(
            workspace=validated_data['workspace'],
            tag=validated_data['tag']
        )
        return t
    
    class Meta:
        model = Tag
        fields =('workspace', 'tag')

class AiResponseSerializer(serializers.ModelSerializer):
    source = SourceSerializer(read_only=True)
    source_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        r = AiResponse.objects.create(
            source=validated_data['source'],
            summary=validated_data['summary'],
            entities=validated_data['entities'],
            locations=validated_data['locations']
        )
        return r
    
    class Meta:
        model = AiResponse
        fields = ('id', 'source', 'summary', 'entities', 'locations', 'source_id')

class RevisionSerializer(serializers.ModelSerializer):
    original_response = AiResponseSerializer(read_only=True)
    workspace = WorkspaceSerializer(read_only=True)
    
    def create(self, validated_data):
        r = Revision.objects.create(
            summary=validated_data['summary'],
            entities=validated_data['entities'],
            locations=validated_data['locations'],
            original_response=validated_data['original_response'],
            workspace=validated_data['workspace']
        )
        return r
    
    class Meta:
        model = Revision
        fields = ('id', 'summary', 'entities', 'locations', 'original_response', 'workspace')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceQuestions
        fields = '__all__'
