from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from course.models import Course
from users.models import User


def courses_view(request):
    courses_list = Course.objects.all()
    paginator = Paginator(courses_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        courses = paginator.page(page_number)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {'courses': courses}
    return render(request, 'courses/course/courses_list.html', context)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'class_association', 'teacher', 'dayofweek', 'hour', 'semester']


def add_course_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course:courses')
    else:
        form = CourseForm()

    return render(request, 'courses/course/add_course.html', {'form': form})


def teacher_courses(request):
    teacher = request.user
    current_day = timezone.now().strftime('%A').lower()
    courses = Course.objects.filter(teacher=teacher, dayofweek=current_day)
    context = {
        'courses': courses,
    }
    return render(request, 'courses/course/today_courses.html', context)


def schedule(request):
    student = get_object_or_404(User, id=request.user.id)
    student_class = student.classe
    courses = Course.objects.filter(class_association=student_class)
    schedule_dict = {}
    for course in courses:
        day = course.get_dayofweek_display()
        hour = course.get_hour_display()
        if day not in schedule_dict:
            schedule_dict[day] = {}
        schedule_dict[day][hour] = course
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    hours = ['9h00 - 12h15', '13h15 - 16h30']
    print('schedule_dict')
    print(schedule_dict)
    return render(request, 'courses/course/schedule.html',
                  {'schedule_dict': schedule_dict, 'days': days, 'hours': hours})
