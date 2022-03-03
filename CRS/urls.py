from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'CRS'

urlpatterns = [
    path('', views.index, name='index'),
    path('professor/list/<int:professor_id>/',
         views.professor_detail, name='professor_detail'),
    path('professor/create/', views.professor_create, name='professor_create'),
    path('professor/list/', views.professor_list, name='professor_list'),
    path('student/list/', views.student_list, name='student_list'),
    path('student/list/<int:student_id>/',
         views.student_detail, name='student_detail'),
    path('student/create/', views.student_create, name='student_create'),
    path('subject/list/', views.subject_list, name='subject_list'),
    path('subject/create/', views.subject_create, name='subject_create'),
    path('signup/list', views.signup_list, name='signup_list'),

    path('login/', auth_views.LoginView.as_view(template_name='CRS/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='CRS/logout.html'), name='logout'),

    path('attendance_create/', views.attendance_create, name='attendance_create'),
    path('attendance_remove/', views.attendance_remove, name='attendance_remove'),

]
