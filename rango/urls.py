from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('teacher_register/', views.teacher_register, name='teacher_register'),
    path('student_register/', views.student_register, name='student_register'),
    path('login/', views.user_login, name='login'),
    path('create_attendance/', views.create_attendance, name='create_attendance'),
    path('teacher_home/', views.teacher_home, name='teacher_home'),
    path('student_home/', views.student_home, name='student_home'),
    path('sign_attendance/', views.sign_attendance, name='sign_attendance'),
    path('overall_attendance/', views.overall_attendance, name='overall_attendance'),
    path('check_attendance/', views.check_attendance, name='check_attendance'),
    path('base/', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('logout/', views.user_logout, name='logout'),
    path('sign_successfully', views.sign_successfully, name='sign_successfully'),

]
