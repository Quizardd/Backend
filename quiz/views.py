from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from quiz.serializers import *
import requests
from django.http.response import JsonResponse, HttpResponse

from quiz.models import *

@api_view(['PUT'])
def GetUser(request):
    uid = request.GET.get('uid')
    type = request.GET.get('type')

    if type == "signin":
        activeuserobj = User.objects.get(uid=uid)

    if type == "signup":
        activeuserobj = User.objects.create(uid=uid)
    
    gen_serializer = UserSerializer(activeuserobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['GET'])
def GetQuizList(request):
    uid = request.GET.get('uid')
    activeuserobj = User.objects.get(uid=uid)

    quizobj = Quiz.objects.filter(user = activeuserobj).order_by('id')
    gen_serializer = QuizSerializer(quizobj, many=True).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['GET'])
def GetQuiz(request):
    id = request.GET.get('id')

    quizobj = Quiz.objects.get(id=id)
    gen_serializer = QuizSerializer(quizobj).data

    return JsonResponse(gen_serializer, safe=False)


@api_view(['POST'])
def CreateQuiz(request):
    uid = request.GET.get('uid')
    activeuserobj = User.objects.get(uid=uid)

    title = request.data.get('title')
    nosofquestions = request.data.get('nosofquestions')
    shuffleQuestion = request.data.get('shuffleQuestion')
    shuffleOptions = request.data.get('shuffleOptions')
    start = request.data.get('start')
    end = request.data.get('end')

    quizobj = Quiz.objects.create(user = activeuserobj, title = title, start = start, end = end, shuffleQuestion = shuffleQuestion, shuffleOptions = shuffleOptions, nosofquestions = nosofquestions)
    gen_serializer = QuizSerializer(quizobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['GET'])
def GetQuestionList(request):
    id = request.GET.get('id')
    quizobj = Quiz.objects.get(id=id)

    questionobj = Question.objects.filter(quiz_list = quizobj).order_by('updated_at')
    gen_serializer = QuestionSerializer(questionobj, many=True).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['POST'])
def CreateQuestion(request):
    uid = request.GET.get('uid')
    activeuserobj = User.objects.get(uid=uid)

    id = request.GET.get('id')
    quizobj = Quiz.objects.get(id=id)

    question = request.data.get('question')
    option1 = request.data.get('option1')
    option2 = request.data.get('option2')
    option3 = request.data.get('option3')
    option4 = request.data.get('option4')
    answer1 = request.data.get('answer1')
    answer2 = request.data.get('answer2')
    answer3 = request.data.get('answer3')
    answer4 = request.data.get('answer4')


    questionobj = Question.objects.create(user = activeuserobj)
    questionobj.quiz_list.add(quizobj)
    gen_serializer = QuestionSerializer(questionobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['GET'])
def GetQuestion(request):
    id = request.GET.get('id')

    quizobj = Question.objects.get(id=id)
    gen_serializer = QuestionSerializer(quizobj).data

    return JsonResponse(gen_serializer, safe=False)


