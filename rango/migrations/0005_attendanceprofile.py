# Generated by Django 2.1.5 on 2020-09-04 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0004_classprofile_courseprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classID', models.IntegerField(default=-1)),
                ('studentID', models.CharField(max_length=128)),
                ('studentName', models.CharField(max_length=128)),
            ],
        ),
    ]
