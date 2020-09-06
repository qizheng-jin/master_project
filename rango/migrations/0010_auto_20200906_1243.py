# Generated by Django 2.1.5 on 2020-09-06 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0009_auto_20200906_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceprofile',
            name='classID',
            field=models.ForeignKey(on_delete=True, to='rango.ClassProfile', to_field='classID'),
        ),
        migrations.AlterField(
            model_name='attendanceprofile',
            name='studentID',
            field=models.ForeignKey(on_delete=True, to='rango.StudentProfile', to_field='studentID'),
        ),
        migrations.AlterField(
            model_name='classprofile',
            name='courseID',
            field=models.ForeignKey(on_delete=True, to='rango.CourseProfile', to_field='courseID'),
        ),
        migrations.AlterField(
            model_name='classprofile',
            name='teacherID',
            field=models.ForeignKey(on_delete=True, to='rango.TeacherProfile', to_field='teacherID'),
        ),
    ]