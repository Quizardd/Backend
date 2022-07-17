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

class Consumer(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "consumer"
    
    def __str__(self):
        return str(self.uid) 

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='QUIZUSER', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nosofquestions = models.IntegerField(blank=True, null=True)
    shuffleQuestion = models.BooleanField(default=False)
    shuffleOptions = models.BooleanField(default=False)

    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    duration = models.IntegerField(blank=True, null=True)

    correct = models.IntegerField(blank=True, null=True, default = 1)
    wrong = models.IntegerField(blank=True, null=True, default = 0)

    status = models.BooleanField(default=False)
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

    tag_list = models.ManyToManyField('Tag', related_name='QUESTIONTAGLIST')
    
    class Meta:
        db_table = "question"
    
    def __str__(self):
        return str(self.id) 

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='TAGUSER', on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, related_name='TAGQUESTION', on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, related_name='TAGQUIZ', on_delete=models.CASCADE, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "tag"

class QuestionResponse(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Consumer, related_name='QUESTIONRESPONSEUSER', on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, related_name='QUESTIONRESPONSEQUIZ', on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, related_name='QUESTIONRESPONSEQUESTION', on_delete=models.CASCADE, blank=True, null=True)
    response1 = models.BooleanField(default=False)
    response2 = models.BooleanField(default=False)
    response3 = models.BooleanField(default=False)
    response4 = models.BooleanField(default=False)
    result = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.response1 == self.question.answer1 and self.response2 == self.question.answer2 and self.response3 == self.question.answer3 and self.response4 == self.question.answer4:
            self.result = True
        else:
            self.result = False
        super(QuestionResponse, self).save(*args, **kwargs)
    
    class Meta:
        db_table = "questionresponse"


class QuizResponse(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='QUIZRESPONSEUSER', on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(Quiz, related_name='QUIZRESPONSEQUIZ', on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True, default=0)

    @property
    def get_score(self):
        correct = self.quiz.correct
        wrong = self.quiz.wrong
        x = QuestionResponse.objects.filter(user = self.user, quiz = self.quiz)
        print(len(x))
        for i in x:
            if i.result == True:
                self.score += correct
            else:
                self.score -= wrong
        return self.score
    
    def save(self, *args, **kwargs):
        self.score = self.get_score
        super(QuizResponse, self).save(*args, **kwargs)

    class Meta:
        db_table = "quizresponse"

