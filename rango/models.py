from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    teacherID = models.CharField(max_length=10, default='', unique=True)
    teacherName = models.CharField(max_length=128, default='')
    course = models.CharField(max_length=128, default='')
    emailAddress = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.teacherID


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    studentID = models.CharField(max_length=10, default='', unique=True)
    studentName = models.CharField(max_length=128, default='')
    emailAddress = models.CharField(max_length=128, default='')
    belongingClass = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.studentID


class CourseProfile(models.Model):
    courseID = models.CharField(default='', unique=True, max_length=128)
    courseName = models.CharField(default='', max_length=128)


class ClassProfile(models.Model):
    classID = models.IntegerField(default=-1, unique=True)
    teacherID = models.CharField(max_length=128, default='')
    courseID = models.CharField(default='', max_length=128)
    Date = models.DateField()
    numOfStudents = models.IntegerField(default=0)


class AttendanceProfile(models.Model):
    classID = models.IntegerField(default=-1)
    studentID = models.CharField(max_length=128)
    studentName = models.CharField(max_length=128)

    class Meta:
        unique_together = ("classID", "studentID")

