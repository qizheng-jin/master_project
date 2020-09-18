from django.contrib.auth.models import User
from django.db import models

# Create your models here.
'''
This is the Teaecher Model, which contains five attributes. User is a foreign key to default User model. teacherID is
the primary key, which represents an unique attribute for Teacher model. Teacher name, course and emailAddress are 
non-primary key.
'''
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    teacherID = models.CharField(max_length=10, default='', unique=True)
    teacherName = models.CharField(max_length=128, default='')
    course = models.CharField(max_length=128, default='')
    emailAddress = models.EmailField(default='empty@emailaddress.com')

    def __str__(self):
        return self.teacherID


'''
This is the Student model, which is similar to the Teacher model. Student ID is the primary key and studentName,
emailAddress and belongingClass is the non-primary key. BelongingClass means to which class does this student belong.
This system contains three options: class1, class2 and class3. Students must choose one of them during registration.
'''
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    studentID = models.CharField(max_length=10, default='', unique=True)
    studentName = models.CharField(max_length=128, default='')
    emailAddress = models.EmailField(default='empty@emailaddress.com')
    belongingClass = models.CharField(max_length=128, default='class1')

    def __str__(self):
        return self.studentID


'''
This is the Course Model, which should be automatically populated into database using populate_rango.py.
We have three default course in the system: IT, DB and Internet. 
'''
class CourseProfile(models.Model):
    courseID = models.CharField(default='', unique=True, max_length=128)
    courseName = models.CharField(default='', max_length=128)


'''
As you may aware, the word 'class' may have two different meanings in this system.
One is the belongingClass in Student Model. Student should choose 'Class1' 'Class2' or 'Class3'
Another represents the ClassProfile model. This model actually stored the information of ClassProfile.
When teachers generated class attendance lists. they actually generate a new entity of this model.
ClassID is a randomly generated number stored, meanwhile it is also the primary key of this model.
taecherID and courseID are two foreign keys pointing to Course model and Teacher model.
Therefore, I want to emphasize that 'class1' 'class2', and 'class3' are not the ClassID.
ClassID should be a 3 digits number like '375', '462'.....
'''
class ClassProfile(models.Model):
    classID = models.IntegerField(default=-1, unique=True)
    teacherID = models.CharField(max_length=128, default='')
    courseID = models.CharField(default='', max_length=128)
    Date = models.DateField()
    '''How many present students'''
    numOfStudents = models.IntegerField(default=0)
    belongingClass = models.CharField(max_length=128, default='class1')


'''
This is the Attendance Model. When students sign attendance, they eventually create a new entity of this model.
It contains three attributes. ClassID and studentID together to be the composite key. ClassID is the foreign key
to Class Profile and StudentID is the foreign key to student profile.
'''
class AttendanceProfile(models.Model):
    classID = models.IntegerField(default=-1)
    studentID = models.CharField(max_length=128)
    studentName = models.CharField(max_length=128)

    class Meta:
        unique_together = ("classID", "studentID")

