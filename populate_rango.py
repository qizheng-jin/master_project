import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'class_attendance_project.settings')
import django
django.setup()
from rango.models import CourseProfile

'''
This function will automatically populate the Course model in database.
Three Course we have for this project: IT, DB and Internet.
'''
def populate():
    course_list = [
        {
            "courseID": "01_Information_Technology",
            "courseName": "Information Technology"
        },
        {
            "courseID": "02_Database",
            "courseName": "Database"
        },
        {
            "courseID": "03_Internet",
            "courseName": "Internet"
        },
    ]

    for c in course_list:
        add_course(c["courseID"], c["courseName"])
        print(str(c))


'''
This is the add_course function
'''
def add_course(courseID, courseName):
    new_course = CourseProfile.objects.get_or_create(courseID=courseID, courseName=courseName)[0]
    new_course.save()
    return new_course


'''
This is the main function
'''
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()

