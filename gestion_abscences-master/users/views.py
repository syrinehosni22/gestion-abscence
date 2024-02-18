from django.contrib.auth import authenticate, login, logout, get_user_model
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.urls import reverse

from classes.models import Class
from users.models import User


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('absence:myAbsences')
        elif request.user.role == 'teacher':
            return redirect('course:todayCourses')
        elif request.user.role == 'admin':
            return redirect(reverse('users:user_type', args=['teacher']))
        else:
            return redirect(reverse('users:account', args=[request.user.id]))

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                if user.role == 'student':
                    return redirect('absence:myAbsences')
                elif user.role == 'teacher':
                    return redirect('course:todayCourses')
                elif user.role == 'admin':
                    return redirect(reverse('users:user_type', args=['teacher']))
                else:
                    return redirect(reverse('users:account', args=[user.id]))

    form = AuthenticationForm()
    return render(
        request=request,
        template_name="users/user/signin.html",
        context={"form": form}
    )


def logout_view(request):
    logout(request)
    return redirect(reverse('users:login'))


def users_view(request, user_type):
    users_list = User.objects.filter(role=user_type)
    paginator = Paginator(users_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        users = paginator.page(page_number)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {'users': users, 'user_type': user_type}
    return render(request, 'users/user/users.html', context)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email, please', required=True)
    profile_image = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'profile_image']

    def __init__(self, user_type, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.user_type = user_type
        if self.user_type == 'student':
            self.fields['classe'] = forms.ModelChoiceField(
                queryset=Class.objects.all(),
                required=True,
            )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.user_type
        user.profile_image = self.cleaned_data['profile_image']
        if self.user_type == 'student':
            user.classe = self.cleaned_data['classe']
        if commit:
            user.save()
        return user


@login_required
def register_view(request, user_type):
    if request.method == "POST":
        form = UserRegistrationForm(user_type, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:user_type', args=[user_type]))
    else:
        form = UserRegistrationForm(user_type)
    return render(
        request=request,
        template_name="users/user/signup.html",
        context={"form": form, 'user_type': user_type}
    )


class UserEditForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        if self.instance.role == 'student':
            self.fields['classe'] = forms.ModelChoiceField(
                queryset=Class.objects.all(),
                required=True,
                initial=self.instance.classe
            )

    def clean_classe(self):
        if self.instance.role == 'teacher':
            return self.instance.classe
        return self.cleaned_data['classe']

    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        if self.instance.role == 'student':
            user.classe = self.cleaned_data['classe']
        if commit:
            user.save()
        return user


def edit_user_view(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if request.FILES.get('profile_image'):
                user.profile_image = request.FILES['profile_image']
            form.save()
            return redirect(reverse('users:user_type', args=[user.role]))
    else:
        form = UserEditForm(instance=user)

    return render(
        request=request,
        template_name='users/user/edit.html',
        context={'form': form, 'user': user}
    )


def delete_user_view(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect(reverse('users:user_type', args=[user.role]))

    return render(
        request=request,
        template_name='users/user/delete.html',
        context={'user': user}
    )


class UserAccountForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self, commit=True):
        user = super(UserAccountForm, self).save(commit=False)
        if commit:
            user.save()
        return user


def account_view(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        form = UserAccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if request.FILES.get('profile_image'):
                user.profile_image = request.FILES['profile_image']
            form.save()
            return redirect(reverse('users:account', args=[user.id]))
    else:
        form = UserAccountForm(instance=user)

    return render(
        request=request,
        template_name='users/user/account.html',
        context={'form': form, 'user': user}
    )
