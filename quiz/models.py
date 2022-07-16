from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    uid = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    product = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    adminuser = models.BooleanField(default=False)

    class Meta:
        db_table = "user"
    
    def __str__(self):
        return str(self.id) 

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='QUIZUSER', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nosofquestions = models.IntegerField(blank=True, null=True)
    shuffleQuestion = models.BooleanField(default=False)
    shuffleOptions = models.BooleanField(default=False)

    start = models.DateTimeField()
    end = models.DateTimeField()

    past = models.BooleanField(default=False)
    live = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=True)
    
    class Meta:
        db_table = "quiz"
    
    def __str__(self):
        return str(self.id) 


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='QUESTIONUSER', on_delete=models.CASCADE, blank=True, null=True)
    quiz_list = models.ManyToManyField(Quiz)

    question = models.CharField(max_length=255, blank=True, null=True)
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    answer1 = models.BooleanField(default=False)
    answer2 = models.BooleanField(default=False)
    answer3 = models.BooleanField(default=False)
    answer4 = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "question"
    
    def __str__(self):
        return str(self.id) 
