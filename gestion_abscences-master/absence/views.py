import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from absence.models import Absence
from course.models import Course
from users.models import User


def take_attendance_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = User.objects.filter(role='student', classe=course.class_association)
    current_date = datetime.date.today()

    absent_students = Absence.objects.filter(course=course, date=current_date).values_list('student_id', flat=True)

    return render(request, 'absence/take_attendance.html', {
        'course': course,
        'students': students,
        'current_date': current_date,
        'absent_students': absent_students,
    })


def save_attendance_view(request, course_id):
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        current_date = datetime.date.today()
        for student in course.class_association.user_set.filter(role='student'):
            is_absent = request.POST.get(f'student_{student.id}') == 'on'
            absence_exists = Absence.objects.filter(student=student, course=course, date=current_date).exists()
            if is_absent:
                if not absence_exists:
                    Absence.objects.create(student=student, course=course, date=current_date)
            else:
                if absence_exists:
                    Absence.objects.filter(student=student, course=course, date=current_date).delete()
        return redirect(reverse('absence:takeAttendance', args=[course_id]))
    else:
        return HttpResponseRedirect(reverse('absence:takeAttendance', args=[course_id]))


def my_absences_view(request):
    absences_list = Absence.objects.filter(student=request.user).order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(absences_list, 10)
    try:
        absences = paginator.page(page)
    except PageNotAnInteger:
        absences = paginator.page(1)
    except EmptyPage:
        absences = paginator.page(paginator.num_pages)

    return render(request, 'absence/student_absences.html', {'absences': absences})
