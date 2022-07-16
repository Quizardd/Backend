from django.urls import path
from quiz import views

urlpatterns = [

    path('getuser/', views.GetUser),
    path('getquizlist/', views.GetQuizList),
    path('getquiz/', views.GetQuiz),
    path('createquiz/', views.CreateQuiz),
    path('getquestionlist/', views.GetQuestionList),
    path('createquestion/', views.CreateQuestion),
    path('getquestion/', views.GetQuestion),
]
