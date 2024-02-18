from django.urls import path

from . import views

app_name = 'absence'
urlpatterns = [
    path('takeAttendance/<int:course_id>', views.take_attendance_view, name='takeAttendance'),
    path('saveAttendance/<int:course_id>', views.save_attendance_view, name='saveAttendance'),
    path('myAbsences/', views.my_absences_view, name='myAbsences'),
]
