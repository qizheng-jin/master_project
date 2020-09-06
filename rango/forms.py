from django.contrib.auth.models import User
from django import forms
from django.forms import widgets

from rango import models
from rango.models import TeacherProfile, StudentProfile, ClassProfile


class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ('teacherID', 'teacherName', 'course', 'emailAddress')


class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class StudentProfileForm(forms.ModelForm):
    select_value = (
        ('class1', 'class1'),
        ('class2', 'class2'),
        ('class3', 'class3'),
    )
    belongingClass = forms.CharField(max_length=128, help_text='Please choose your class',
                                     widget=widgets.Select(choices=select_value))

    class Meta:
        model = StudentProfile
        fields = ('studentID', 'studentName', 'emailAddress', 'belongingClass')


class ClassProfileForm(forms.ModelForm):
    select_value = (
        ('01_Information_Technology', 'Information Technology'),
        ('02_Database', 'Database'),
        ('03_Internet', 'Internet'),
    )

    teacherID = forms.CharField(max_length=128, help_text="Please enter your teacher ID")
    courseID = forms.CharField(widget=widgets.Select(choices=select_value), help_text="Please enter your course ID")
    Date = forms.DateField(widget=forms.SelectDateWidget, help_text="Enter the course date")


    class Meta:
        model = ClassProfile
        fields =('teacherID', 'courseID', 'Date')
