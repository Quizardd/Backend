from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'user'
        model = User
        abstract = True
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'quiz'
        model = Quiz
        abstract = True
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'question'
        model = Question
        abstract = True
        fields = '__all__'