from django.contrib import admin
from .models import Professor
from .models import Student
from .models import Subject
from .models import Attendance
from .models import Users

# Register your models here.


# 커스텀 유저 모델(Custom User Model)이 관리자 화면에 어떻게 표시할지를 설정

class ProfessorAdmin(admin.ModelAdmin):
    search_fields = ['name']


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['name']


class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['subject_name']


class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ['subject_code']

# Users 모델에 세부 기능을 추가할 수 있는 Users 클래스를 생성하고 제목 검색을 위해 search_fields 속성에 username을 추가


class UsersAdmin(admin.ModelAdmin):
    search_fields = ['username']


# 검색 값 등록
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Users, UsersAdmin)
