# Generated by Django 4.0.6 on 2022-07-16 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_question_answer_question_answer1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='upcoming',
            field=models.BooleanField(default=True),
        ),
    ]