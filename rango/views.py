import random

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from rango.forms import TeacherForm, TeacherProfileForm, StudentForm, StudentProfileForm, ClassProfileForm
from rango.models import TeacherProfile, ClassProfile, AttendanceProfile, CourseProfile, StudentProfile

'''
This is the index function
'''
def index(request):
    return render(request, 'rango/index.html', {})

'''
This is the About Us function
'''
def about(request):
    return render(request, 'rango/about.html')


'''
This is the teacher registration funtion, it will take TeacherForm and Teacher ProfileForm results and analyze them.
TeacherForm will be saved as the user information. TeacherProfileForm will be saved as the basic information for teachers
'''
def teacher_register(request):
    registered = False

    if request.method == 'POST':
        user_form = TeacherForm(request.POST)
        profile_form = TeacherProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = TeacherForm()
        profile_form = TeacherProfileForm()

    return render(request, 'rango/teacher_register.html', {'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'registered': registered})


'''
Register for students is similar to register for teachers.
StudentForm contains username and passwords; StudentProfileForm contains student basic information.
'''
def student_register(request):
    registered = False

    if request.method == 'POST':
        user_form = StudentForm(request.POST)
        profile_form = StudentProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = StudentForm()
        profile_form = StudentProfileForm()

    return render(request, 'rango/student_register.html', {'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'registered': registered})


'''
This is the function for user logging in. The Algorithm for this is:

1. get the username and password
2. check whether this account is valid
    2.1 If user account is not valid, print error information
    2.2 If user account is valid, log in to the system then:
        2.2.1   Check whether Teacher Model contains this user
            2.2.1.1 If this user is a teacher account, redirect users to 'teacher_home'
            2.2.1.2 If this user is not a student account, which means it should be a student account
                    therefore, redirect users to 'student_home'
'''
def user_login(request):
    context_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            '''Check if user account is valid'''
            if user.is_active:
                login(request, user)
                '''Try to find whether this user is a teacher account'''
                try:
                    teachers = TeacherProfile.objects.get(user=user)
                    context_dict['teacher'] = teachers
                    '''If not then is is a student account'''
                except TeacherProfile.DoesNotExist:
                    teachers = None
                    student = StudentProfile.objects.get(user=user)
                    context_dict['student'] = student
                if teachers is not None:
                    return redirect(reverse('rango:teacher_home'))
                else:
                    return redirect(reverse('rango:student_home'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})

'''
This is the logout method
'''
def user_logout(request):
    logout(request)
    return render(request, 'rango/logout.html', {})

'''
This is the teacher_home method, it detects the users' teacher ID and name, which will be used on front ends.
'''
def teacher_home(request):
    context_dict={}
    if request.user.is_authenticated:
        teacher = TeacherProfile.objects.get(user=request.user)
        context_dict['teacher'] = teacher
        return render(request, 'rango/teacher_home.html', context=context_dict)
    return render(request, 'rango/teacher_home.html', context=context_dict)


'''
Here shows the algorithm of create the attendance lists:
1. Set classes as all class objects in Class model, 
    set teacher to all teacher objects in Teacher Model
2. Get the courseID, Date and belongingClass in ClassProfileForm on front ends.
3. Start to generate a random number to represent Class ID, which must be unique in Class model in database:
    3.1 generate an loop stop checker called out = False.
    3.2 While out is False:
        3.2.1 set out to True
        3.2.2 generate a random number from 0 to 999, called cid
        3.2.3 for all classes, check whether their class IDs are the same with cid:
            3.2.3.1 If they have the same ID, change set = False
4.  Save the Class ID and set the default numOfStudents = 0
5.  Save the new class entity
'''
def create_attendance(request):
    context_dict = {}
    classes = ClassProfile.objects.all()
    finish = False
    teacher = ''
    if request.user.is_authenticated:
        teacher = TeacherProfile.objects.get(user=request.user)
        context_dict['teacher'] = teacher
    if request.method == 'POST':
        class_form = ClassProfileForm(request.POST)
        if class_form.is_valid():
            new_class = class_form.save(commit=False)
            out = False
            cid = 0
            while out is not True:
                out = True
                cid = random.randint(0, 999)
                for c in classes:
                    if c.classID == cid:
                        out = False
            new_class.teacherID = teacher.teacherID
            new_class.classID = cid
            new_class.numOfStudents = 0
            context_dict['cid'] = cid
            new_class.save()
            finish = True
            context_dict['finish'] = finish
            return render(request, 'rango/create_attendance.html', context=context_dict)
        else:
            print(class_form.errors)
    else:
        class_form = ClassProfileForm(request.POST)
        context_dict['class_form'] = class_form
    context_dict['finish'] = finish
    return render(request, 'rango/create_attendance.html', context=context_dict)


'''
Student Home need to search right classes to sign attendance, The algorithm for this is shown below:
1. check the account information. get the student ID and student name.
2.  get the class ID students input from front ends.
3. Check if this class ID is valid:
    3.1 If this class ID is valid, compare whether they have the same belongingClass:
        3.1.1 if they have the same belongingClass attributes, it means this student belongs to this class
            therefore he can sign the attendance.
            3.1.1.1 get all class information together with this students' information send them to the sign_attendance page
        3.1.2 If they have different belongingClass attributes, this student can not sign the attendances, print errors.
    3.2 If this class ID is not valid, print errors
'''
def student_home(request):
    context_dict = {}
    if request.method == 'POST':
        classid = request.POST.get('classid')
        context_dict['classid'] = classid
        if request.user.is_authenticated:
            student = StudentProfile.objects.get(user=request.user)
            studentid = student.studentID
            studentname = student.studentName
            context_dict['studentid'] = studentid
            context_dict['studentname'] = studentname
            try:
                this_class = ClassProfile.objects.get(classID=classid)
                if this_class.belongingClass == student.belongingClass:
                    courseID = this_class.courseID
                    this_course = CourseProfile.objects.get(courseID=courseID)
                    courseName = this_course.courseName
                    teacherid = this_class.teacherID
                    course_date = this_class.Date
                    date = str(course_date)
                    context_dict['classname'] = courseName
                    context_dict['teacherid'] = teacherid
                    context_dict['date'] = date
                    return render(request, 'rango/sign_attendance.html', context=context_dict)
                else:
                    context_dict['wrongclass'] = True
                    return render(request, 'rango/student_home.html', context=context_dict)
            except ClassProfile.DoesNotExist:
                context_dict['not_found'] = True
                context_dict['does_not_exist'] = 'Your Class ID Does Not Exist'
                return render(request, 'rango/student_home.html', context=context_dict)
    return render(request, 'rango/student_home.html', {})


'''
This is the method for signing attendance, here shows the algorithm:
1.  get the classid, studentid and studentname from front ends.
2.  create a new Attendance entity based on information above.
3.  Compare this new attendance entity with all existing entities in Attendance Model:
    3.1 If this entity is duplicated, print the error.
    3.2 If not, save this new attendance in database
'''
def sign_attendance(request):
    context_dict = {}

    if request.method == 'POST':
        classid = request.POST.get('classid')
        studentid = request.POST.get('studentid')
        studentname = request.POST.get('studentname')
        context_dict['studentid'] = studentid
        context_dict['studentname'] = studentname
        try:
            AttendanceProfile.objects.create(classID=classid, studentID=studentid, studentName=studentname)
            this_class = ClassProfile.objects.get(classID=classid)
            this_class.numOfStudents = this_class.numOfStudents + 1
            this_class.save()
            return render(request, 'rango/sign_successfully.html', context=context_dict)
        except:
            context_dict['errors'] = 'You cannot sign one class twice!'
            return render(request, 'rango/sign_attendance.html', context=context_dict)
    return render(request, 'rango/sign_attendance.html', context=context_dict)


'''
This is the overall attendance function. This function will pass all class entities with this teacher to front end.
Meanwhile, it will pass all class sizes for three classes to calculate the attendance rates
'''
def overall_attendance(request):
    context_dict = {}
    if request.user.is_authenticated:
        teacher = TeacherProfile.objects.get(user=request.user)
        classes = ClassProfile.objects.filter(teacherID=teacher.teacherID)
        numOfClassOne = StudentProfile.objects.filter(belongingClass='class1').count()
        numOfClassTwo = StudentProfile.objects.filter(belongingClass='class2').count()
        numOfClassThree = StudentProfile.objects.filter(belongingClass='class3').count()
        context_dict['numOfClassOne'] = numOfClassOne
        context_dict['numOfClassTwo'] = numOfClassTwo
        context_dict['numOfClassThree'] = numOfClassThree
        context_dict['classes'] = classes
        return render(request, 'rango/overall_attendance.html', context=context_dict)
    return render(request, 'rango/overall_attendance.html', context=context_dict)


'''
This is the check_attendance method. The aim of this is to find the absent students in one exact class.
The methodology for this is:
1.  Get the classID as cid and belongingClass as bc from front page.
2. Find the attendance entities in the Attendance model, if they get the same classID with the cid,
    It means those students have participated this class.
3.  Find all students in Student Model, who get the same class Belonging with the bc. These are overall student lists
    who should be in class.
4.  Find the difference between the present student lists with overall student lists, which are the absent students
'''
def check_attendance(request):
    context_dict = {}
    if request.method == 'POST':
        classid = request.POST.get('classid')
        belonging_class = request.POST.get('belonging_class')
        in_class = AttendanceProfile.objects.filter(classID=classid).values('studentID', 'studentName')
        student_list = StudentProfile.objects.filter(belongingClass=belonging_class).values('studentID', 'studentName')
        absent_list = student_list.difference(in_class)
        context_dict['all_students'] = student_list
        context_dict['in_class'] = in_class
        context_dict['absent'] = absent_list
        return render(request, 'rango/check_attendance.html', context=context_dict)
    return render(request, 'rango/check_attendance.html', context=context_dict)


def base(request):
    return render(request, 'rango/base.html', {})


'''
This is the sign in successfully function.
'''
def sign_successfully(request):
    return render(request, 'sign_successfully.html', {})