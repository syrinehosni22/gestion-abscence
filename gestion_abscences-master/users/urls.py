from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('account/<int:user_id>/', views.account_view, name='account'),
    path('<str:user_type>/', views.users_view, name='user_type'),
    path('register/<str:user_type>/', views.register_view, name='register'),
    path('edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('delete/<int:user_id>', views.delete_user_view, name='delete_user'),
]
