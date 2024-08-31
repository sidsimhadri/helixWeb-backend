from rest_framework import serializers
from .models import Question
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  

    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'thumbs_up', 'thumbs_down', 'user']
        read_only_fields = ['id']

