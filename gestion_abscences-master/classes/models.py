from django.db import models


class Class(models.Model):
    Category = (
        ('1 ère', '1 ère'),
        ('2 ème', '2 ème'),
        ('3 ème', '3 ème'),
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=Category)

    def __str__(self):
        return f"{self.category} - {self.name}"
