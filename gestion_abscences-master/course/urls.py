from django.urls import path

from . import views

app_name = 'course'
urlpatterns = [
    path('courses/', views.courses_view, name='courses'),
    path('addCourse/', views.add_course_view, name='addCourse'),
    path('todayCourses/', views.teacher_courses, name='todayCourses'),
    path('schedule/', views.schedule, name='schedule'),
]
