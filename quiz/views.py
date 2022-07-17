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
    quizid = request.GET.get('quizid')

    quizobj = Quiz.objects.get(id=quizid)
    gen_serializer = QuizSerializer(quizobj).data

    return JsonResponse(gen_serializer, safe=False)


@api_view(['POST'])
def CreateQuiz(request):
    uid = request.GET.get('uid')
    activeuserobj = User.objects.get(uid=uid)

    title = request.data.get('title')
    nosofquestions = request.data.get('nosofquestions')
    shuffleQuestion = request.data.get('shuffleQuestion')
    if shuffleQuestion == "True":
        shuffleQuestion = True
    else:
        shuffleQuestion = False
    shuffleOptions = request.data.get('shuffleOptions')
    if shuffleOptions == "True":
        shuffleOptions = True
    else:
        shuffleOptions = False
    start = request.data.get('start')
    end = request.data.get('end')

    correct = request.data.get('correct')
    wrong = request.data.get('wrong')

    duration = request.data.get('duration')

    quizobj = Quiz.objects.create(user = activeuserobj, title = title, start = start, end = end, shuffleQuestion = shuffleQuestion, shuffleOptions = shuffleOptions, nosofquestions = nosofquestions, correct = correct, wrong = wrong, duration = duration)
    gen_serializer = QuizSerializer(quizobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['GET'])
def GetQuestionList(request):
    quizid = request.GET.get('quizid')
    quizobj = Quiz.objects.get(id=quizid)

    print(quizobj.title)
    print(quizobj.shuffleQuestion, type(quizobj.shuffleQuestion))

    if quizobj.shuffleQuestion == True:
        print("True")
        questionobj = Question.objects.filter(quiz_list = quizobj).order_by('?')
    else:
        print("False")
        questionobj = Question.objects.filter(quiz_list = quizobj).order_by('updated_at')
    gen_serializer = QuestionSerializer(questionobj, many=True).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['POST'])
def CreateQuestion(request):
    uid = request.GET.get('uid')
    activeuserobj = User.objects.get(uid=uid)

    quizid = request.GET.get('quizid')
    quizobj = Quiz.objects.get(id=quizid)

    question = request.data.get('question')

    option1 = request.data.get('option1')
    option2 = request.data.get('option2')
    option3 = request.data.get('option3')
    option4 = request.data.get('option4')


    if "answer1" in request.data:
        answer1 = True
    else:
        answer1 = False
    if "answer2" in request.data:
        answer2 = True
    else:
        answer2 = False
    if "answer3" in request.data:
        answer3 = True
    else:
        answer3 = False
    if "answer4" in request.data:
        answer4 = True
    else:
        answer4 = False
    
    tags = request.data.get('tags')
    tags = tags.split(',')

    questionobj = Question(user = activeuserobj, question = question, option1 = option1, option2 = option2, option3 = option3, option4 = option4, answer1 = answer1, answer2 = answer2, answer3 = answer3, answer4 = answer4)
    questionobj.save()
    questionobj.quiz_list.add(quizobj)
    for tag in tags:
        try:
            tagobj = Tag.objects.get(user = activeuserobj, question = questionobj, quiz = quizobj, tag = tag)
        except Tag.DoesNotExist:
            tagobj = Tag.objects.create(user = activeuserobj, question = questionobj, quiz = quizobj, tag = tag)
        
        questionobj.tag_list.add(tagobj)

    gen_serializer = QuestionSerializer(questionobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['GET'])
def GetQuestion(request):
    questionid = request.GET.get('questionid')

    questionobj = Question.objects.get(id=questionid)
    gen_serializer = QuestionSerializer(questionobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['POST'])
def CreateConsumer(request):
    uid = request.GET.get('uid')
    try:
        activeuserobj = Consumer.objects.get(uid=uid)
    except Consumer.DoesNotExist:
        activeuserobj = Consumer.objects.create(uid=uid)

    gen_serializer = ConsumerSerializer(activeuserobj).data 
    return JsonResponse(gen_serializer, safe=False)

@api_view(['POST'])
def SubmitQuestion(request):
    uid = request.GET.get('uid')
    activeuserobj = Consumer.objects.get(uid=uid)

    quizid = request.GET.get('quizid')
    quizobj = Quiz.objects.get(id=quizid)

    questionid = request.GET.get('questionid')
    questionobj = Question.objects.get(id=questionid)

    response1 = True if request.data.get('response1') == "True" else False
    response2 = True if request.data.get('response2') == "True" else False
    response3 = True if request.data.get('response3') == "True" else False
    response4 = True if request.data.get('response4') == "True" else False

    questionresponseobj = QuestionResponse(user = activeuserobj, quiz = quizobj, question = questionobj, response1 = response1, response2 = response2, response3 = response3, response4 = response4)
    questionresponseobj.save()

    gen_serializer = QuestionResponseSerializer(questionresponseobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['POST'])
def SubmitQuiz(request):
    uid = request.GET.get('uid')
    activeuserobj = Consumer.objects.get(uid=uid)

    quizid = request.GET.get('quizid')
    quizobj = Quiz.objects.get(id=quizid)

    quizresponseobj = QuizResponse(user = activeuserobj, quiz = quizobj)
    quizresponseobj.save()

    gen_serializer = QuizResponseSerializer(quizresponseobj).data

    return JsonResponse(gen_serializer, safe=False)

@api_view(['GET'])
def GetAnalysis(request):
    uid = request.GET.get('uid')
    activeuserobj = User.objects.get(uid=uid)

    quizid = request.GET.get('quizid')
    quizobj = Quiz.objects.get(id=quizid)

    tagsobject = Tag.object.filter(uid = uid, quiz = quizobj)

    data = {}

    for i in tagsobject:
        if i.tag in data:
            a = QuestionResponse.objects.get(question = i.question)
            if a.result == True:
                data[i.tag]["correct"] += 1
            else:
                data[i.tag]["wrong"] -= 1
        else:
            a = QuestionResponse.objects.get(question = i.question)
            data[i.tag] = {"correct" : 0, "wrong" : 0}
            if a.result == True:
                data[i.tag]["correct"] += 1
            else:
                data[i.tag]["wrong"] -= 1

    tag_data = {}

    for i in data:
        accuracy = (data[i]["correct"] + data[i]["wrong"]) / (data[i]["correct"] + abs(data[i]["wrong"]))
        tag_data[i] = {"accuracy" : accuracy}
    
    quizresponseobj = QuizResponse.object.get(user = activeuserobj, quiz = quizobj)
    scored = quizresponseobj.score
    total = quizobj.nosofquestions

    data = {"tag" : tag_data, "scored" : scored, "total" : total}

    return JsonResponse(data, safe=False)


