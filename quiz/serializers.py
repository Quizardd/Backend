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

class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'questionresponse'
        model = QuestionResponse
        abstract = True
        fields = '__all__'

class QuizResponseSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'quizresponse'
        model = QuizResponse
        abstract = True
        fields = '__all__'

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'consumer'
        model = Consumer
        abstract = True
        fields = '__all__'