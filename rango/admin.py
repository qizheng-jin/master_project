from django.contrib import admin

# Register your models here.
from rango.models import TeacherProfile, StudentProfile, CourseProfile, AttendanceProfile, ClassProfile

'''
This is the admin page design. Admin page will contain five different data models:
TeacherProfile, StudentProfile, CourseProfile, ClassProfile and AttendanceProfile
All five models with all attributes inside have been shown in admin page.
'''


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacherID', 'teacherName', 'course', 'emailAddress')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentID', 'studentName', 'emailAddress', 'belongingClass')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseID', 'courseName')


class ClassAdmin(admin.ModelAdmin):
    list_display = ('classID', 'courseID', 'teacherID', 'Date', 'numOfStudents', 'belongingClass')


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('classID', 'studentID', 'studentName')


admin.site.register(CourseProfile, CourseAdmin)
admin.site.register(TeacherProfile, TeacherAdmin)
admin.site.register(StudentProfile, StudentAdmin)
admin.site.register(AttendanceProfile, AttendanceAdmin)
admin.site.register(ClassProfile, ClassAdmin)