import random

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from rango.forms import TeacherForm, TeacherProfileForm, StudentForm, StudentProfileForm, ClassProfileForm
from rango.models import TeacherProfile, ClassProfile, AttendanceProfile, CourseProfile, StudentProfile


def index(request):
    return render(request, 'rango/index.html', {})


def about(request):
    context_dict={}
    if request.user.is_authenticated:
        teacherID = TeacherProfile.objects.get(user=request.user).values_list('teacherID', flat=True)
        context_dict['teacherID'] = teacherID
    return render(request, 'rango/about.html', context=context_dict)


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


def user_login(request):
    context_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                try:
                    teachers = TeacherProfile.objects.get(user=user)
                    context_dict['teacher'] = teachers
                except TeacherProfile.DoesNotExist:
                    teachers = None
                    student = StudentProfile.objects.get(user=user)
                    context_dict['student'] = student
                if teachers is not None:
                    return redirect(reverse('rango:teacher_home'))
                else:
                    return render(request, 'rango/student_home.html', context=context_dict)
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


def user_logout(request):
    logout(request)
    return render(request, 'rango/logout.html', {})


def teacher_home(request):
    context_dict={}
    if request.user.is_authenticated:
        teacher = TeacherProfile.objects.get(user=request.user)
        context_dict['teacher'] = teacher
        return render(request, 'rango/teacher_home.html', context=context_dict)
    return render(request, 'rango/teacher_home.html', context=context_dict)


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
        except ClassProfile.DoesNotExist:
            context_dict['not_found'] = True
            context_dict['does_not_exist'] = 'Your Class ID Does Not Exist'
            return render(request, 'rango/student_home.html', context=context_dict)
    return render(request, 'rango/student_home.html', {})


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


def overall_attendance(request):
    context_dict = {}
    if request.user.is_authenticated:
        teacher = TeacherProfile.objects.get(user=request.user)
        classes = ClassProfile.objects.filter(teacherID=teacher.teacherID)
        context_dict['classes'] = classes
        return render(request, 'rango/overall_attendance.html', context=context_dict)
    return render(request, 'rango/overall_attendance.html', context=context_dict)


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


def sign_successfully(request):
    return render(request, 'sign_successfully.html', {})