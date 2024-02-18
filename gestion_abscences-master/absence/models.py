from django.db import models

from course.models import Course
from users.models import User


class Absence(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='absences')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
