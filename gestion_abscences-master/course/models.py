from django.db import models
from users.models import User
from classes.models import Class


class Course(models.Model):
    DAY = [
        ('monday', 'monday'),
        ('tuesday', 'tuesday'),
        ('wednesday', 'wednesday'),
        ('thursday', 'thursday'),
        ('friday', 'friday'),
    ]

    SEMESTER = [
        ('semester1', 'Semester 1'),
        ('semester2', 'Semester 2'),
    ]

    HOURS = [
        ('9h00 - 12h15', '9h00 - 12h15'),
        ('13h15 - 16h30', '13h15 - 16h30'),
    ]

    name = models.CharField(max_length=200)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    class_association = models.ForeignKey(Class, on_delete=models.CASCADE)
    dayofweek = models.CharField(max_length=10, choices=DAY, default='monday')
    hour = models.CharField(max_length=20, choices=HOURS, default='9h00 - 12h15')
    semester = models.CharField(max_length=10, choices=SEMESTER, default='semester1')
