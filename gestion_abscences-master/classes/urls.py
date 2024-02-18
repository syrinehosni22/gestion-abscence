from django.urls import path

from . import views

app_name = 'classes'
urlpatterns = [
    path('classes/', views.classes_view, name='classes'),
    path('addClass/', views.add_class, name='addClass'),
]
