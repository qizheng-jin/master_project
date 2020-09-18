from django.contrib.auth.models import User
from django import forms
from django.forms import widgets

from rango import models
from rango.models import TeacherProfile, StudentProfile, ClassProfile

'''
This is the teacher registration form.  TeacherForm represent the teacher accounts, username and password
'''
class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

'''
This is also the teacher registration form. It include the teacher ID, teacher name, course and email address.
'''
class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ('teacherID', 'teacherName', 'course', 'emailAddress')

'''
This is for student registration, it contains username and password
'''
class StudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

'''
It contains all information about students including studentID, studentName, emailAddress and belonging class.
Belonging class mains which class is this student belong to. In this system, We have three default choice which is 
class1, class2 and class3.
'''
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

'''
This form is used for generating classes. It contains two information courseID and Date, where courseID is an option.
Teachers should choose One of them as the course.
'''
class ClassProfileForm(forms.ModelForm):
    select_value = (
        ('01_Information_Technology', 'Information Technology'),
        ('02_Database', 'Database'),
        ('03_Internet', 'Internet'),
    )
    value = (
        ('class1', 'class1'),
        ('class2', 'class2'),
        ('class3', 'class3'),
    )
    courseID = forms.CharField(widget=widgets.Select(choices=select_value), help_text="Please choose your course name")

    Date = forms.DateField(widget=forms.SelectDateWidget, help_text="Enter the course date")
    belongingClass = forms.CharField(
        widget=widgets.Select(choices=value), help_text="Please choose the class taking this course")

    class Meta:
        model = ClassProfile
        fields =('courseID', 'Date', 'belongingClass')
