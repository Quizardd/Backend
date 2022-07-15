from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    uid = models.IntegerField(null=False)
    role = models.CharField(max_length=50, null=True, blank=True)
    product = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    adminuser = models.BooleanField(default=False)

    class Meta:
        db_table = "user"

class Quiz_list(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='USER', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "quiz_list"


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_list = models.ManyToManyField(Quiz_list)
    question = models.CharField(max_length=255, blank=True, null=True)
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "question"
