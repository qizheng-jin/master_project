# Generated by Django 2.1.5 on 2020-09-04 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0005_attendanceprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='classprofile',
            name='numOfStudents',
            field=models.IntegerField(default=0),
        ),
    ]
