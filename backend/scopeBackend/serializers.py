from rest_framework import serializers
from .models import User, Query, Source, Result, KeyWord

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

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'text', 'url', 'sourceType')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('run_id', 'source_id')
