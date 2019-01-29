from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Message

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'password', 'id')
        extra_kwargs = {'password': {'write_only': True, 'required': True}, 'last_name': {'required': True},
                        'first_name': {'required': True}}

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    last_name = serializers.CharField(read_only=True, source="user.last_name")
    first_name = serializers.CharField(read_only=True, source="user.first_name")
    class Meta:
        model = Message
        fields = ('url', 'id', 'last_name', 'first_name', 'text', 'created')
        extra_kwargs = {'text': {'required': True}}

class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(max_length=128, required=True)