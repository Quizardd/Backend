# Generated by Django 4.0.6 on 2022-07-15 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='quiz_list',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
