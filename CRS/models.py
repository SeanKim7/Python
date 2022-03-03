from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


#  교수
class Professor(models.Model):
    professor_no = models.IntegerField(validators=[MinValueValidator(
        10000), MaxValueValidator(99999)], help_text="교번 5자리를 입력하세요", primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    telno = models.CharField(max_length=30)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Users(AbstractUser):
    user_no = models.IntegerField(null=True)
    user_type = models.CharField(max_length=1, default='0')  # 1: 교수, 2: 학생


# 과목(교수)
class Subject(models.Model):
    subject_code = models.AutoField(primary_key=True) # 과목코드
    professor_no = models.ForeignKey(Professor, on_delete=models.CASCADE) # 교수번호
    subject_name = models.CharField(max_length=80) # 과목명
    maximum_num = models.IntegerField(default=30)  # 제한인원
    current_num = models.IntegerField(default=0)   # 현재인원
    lecture_day = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)]) # 강의일
    lecture_time = models.IntegerField(default=100000000)      # 수강시간
    lecture_room = models.CharField(default="A001", max_length=30) # 강의실
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject_name


# 학생
class Student(models.Model):
    student_no = models.IntegerField(validators=[MinValueValidator(
        10000000), MaxValueValidator(99999999)], help_text="학번 8자리를 입력하세요", primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    telno = models.CharField(max_length=30)
    create_date = models.DateTimeField()

    def __str__(self):
        return self.name


# 출석부(과목)
class Attendance(models.Model):
    attendance_code = models.AutoField(primary_key=True)
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False)
    student_no = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
