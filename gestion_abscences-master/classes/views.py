from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from classes.models import Class
from django import forms


def classes_view(request):
    classes_list = Class.objects.all()
    paginator = Paginator(classes_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        classes = paginator.page(page_number)
    except PageNotAnInteger:
        classes = paginator.page(1)
    except EmptyPage:
        classes = paginator.page(paginator.num_pages)

    context = {'classes': classes}
    return render(request, 'classes/class/classes_list.html', context)


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'category']


def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('classes:classes')
    else:
        form = ClassForm()

    return render(request, 'classes/class/add_class.html', {'form': form})