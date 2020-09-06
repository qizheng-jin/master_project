from django.contrib import admin

# Register your models here.
from rango.models import TeacherProfile, StudentProfile, CourseProfile, AttendanceProfile, ClassProfile


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacherID', 'teacherName', 'course', 'emailAddress')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentID', 'studentName', 'emailAddress', 'belongingClass')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseID', 'courseName')


class ClassAdmin(admin.ModelAdmin):
    list_display = ('classID', 'courseID', 'teacherID', 'Date', 'numOfStudents')


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('classID', 'studentID', 'studentName')


admin.site.register(CourseProfile, CourseAdmin)
admin.site.register(TeacherProfile, TeacherAdmin)
admin.site.register(StudentProfile, StudentAdmin)
admin.site.register(AttendanceProfile, AttendanceAdmin)
admin.site.register(ClassProfile, ClassAdmin)