from django import forms
from django.core.validators import MaxValueValidator
from CRS.models import Professor
from CRS.models import Student
from CRS.models import Subject
from CRS.models import Users


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject  # 사용할 모델
        fields = ['subject_code', 'professor_no',
                  'subject_name', 'lecture_day', 'lecture_time', 'lecture_room']  # ProfessorForm에서 사용할 모델의 속성
        widgets = {
            # 'subject': forms.TextInput(attrs={'class': 'form-control'}),
            # 'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject_code': '과목코드',
            'professor_no': '교번',
            'subject_name': '과목이름',
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student  # 사용할 모델
        fields = ['student_no', 'name', 'email',
                  'telno']  # StudentForm 사용할 모델의 속성
        widgets = {
            # 'subject': forms.TextInput(attrs={'class': 'form-control'}),
            # 'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'student_no': '학번',
            'name': '이름',
            'email': '이메일',
            'telno': '전화번호',
        }


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor  # 사용할 모델
        fields = ['professor_no', 'name', 'email',
                  'telno']  # ProfessorForm에서 사용할 모델의 속성
        widgets = {
            # 'subject': forms.TextInput(attrs={'class': 'form-control'}),
            # 'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'professor_no': '교번',
            'name': '이름',
            'email': '이메일',
            'telno': '전화번호',
        }


class RegisterForm_pro(forms.Form):
    professor_no = forms.IntegerField(validators=[MaxValueValidator(
        10000), MaxValueValidator(99999)], label="교번 5자리를 입력하세요")
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    telno = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm_stu(forms.Form):
    student_no = forms.IntegerField(validators=[MaxValueValidator(
        10000000), MaxValueValidator(99999999)], label="학번 8자리를 입력하세요")
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    telno = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
