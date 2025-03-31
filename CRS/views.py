from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Professor
from .forms import ProfessorForm, RegisterForm_pro, RegisterForm_stu
from .models import Student
from .forms import Users
from .models import Users

from .forms import StudentForm
from .models import Subject
from .forms import SubjectForm
from django.db import transaction

from .models import Attendance
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def professor_list(request):
    """ 
    교수 리스트 출력
    """
    professor_list = Professor.objects.order_by('-create_date')
    context = {'professor_list': professor_list}
    return render(request, 'CRS/professor_list.html', context)


def professor_detail(request, professor_id):
    """
    교수 내용 출력
    """
    print("교수 상세내역")
    professor = Professor.objects.get(professor_no=professor_id)
    context = {'professor': professor}
    return render(request, 'CRS/professor_detail.html', context)


def professor_create(request):
    """ 교수 등록 """
    template_name = 'CRS/professor_form.html'

    if request.method == 'POST':
        with transaction.atomic():
            professor = Professor(
                professor_no=request.POST['professor_no'],
                name=request.POST['name'],
                email=request.POST['email'],
                telno=request.POST['telno'],
                create_date=timezone.now(),
            )
            professor.save()
            user = Users(
                username=request.POST['professor_no'],
                email=request.POST['email'],
                is_staff=False,
                is_superuser=False,
                is_active=True,
                user_no=request.POST['professor_no'],
                user_type='1',
            )
            user.set_password(request.POST['password'])
            user.save()
            professor_list = Professor.objects.order_by('-create_date')
            context = {'professor_list': professor_list}
            return render(request, 'CRS/professor_list.html', context)
    else:
        form = RegisterForm_pro()
    context = {'form': form}
    return render(request, template_name, context)


def student_list(request):
    """    학생 리스트 출력    """
    print("학생 리스트 출력 !!!")
    student_list = Student.objects.order_by('-create_date')
    context = {'student_list': student_list}
    return render(request, 'CRS/student_list.html', context)


def student_detail(request, student_id):
    """
    학생 내용 출력
    """
    student = Student.objects.get(student_no=student_id)
    context = {'student': student}
    return render(request, 'CRS/student_detail.html', context)


def student_create(request):
    """ 학생 등록 """
    template_name = 'CRS/student_form.html'

    if request.method == 'POST':
        with transaction.atomic():
            student = Student(
                student_no=request.POST['student_no'],
                name=request.POST['name'],
                email=request.POST['email'],
                telno=request.POST['telno'],
                create_date=timezone.now(),
            )
            student.save()
            user = Users(
                username=request.POST['student_no'],
                email=request.POST['email'],
                is_staff=False,
                is_superuser=False,
                is_active=True,
                user_no=request.POST['student_no'],
                user_type='2',
            )
            user.set_password(request.POST['password'])
            user.save()
            student_list = Student.objects.order_by('-create_date')
            context = {'student_list': student_list}
            return render(request, 'CRS/student_list.html', context)
    else:
        form = RegisterForm_stu()
    context = {'form': form}
    return render(request, template_name, context)


def subject_list(request):
    """
    과목 리스트 출력
    """
    subject_list2 = Subject.objects.filter(professor_no=request.user.user_no)
    context = {'subject_list': subject_list2}
    return render(request, 'CRS/subject_list.html', context)


def subject_create(request):
    """
    과목 등록
    """

    if request.method == 'POST':
        val0 = request.POST['lecture_time']
        val1 = val0.split(',')  # 리스트로 받아온 값을 콤마로 나누어서 리스트로 만들어준다.
        val2 = [int(i) for i in val1]  # 리스트 내부의 값을 숫자로 형변환
        val3 = sum(val2)  # 형변환된 리스트 내의 숫자를 모두 더해서 합을 구한다.
        val4 = str(val3)  # 인덱스를 사용하기 위해 문자열로 형변환
        val5 = val4[1:]  # 첫번째 문자열 삭제

        subject = Subject(
            professor_no_id=request.user.user_no,
            subject_name=request.POST['subject_name'],
            maximum_num=request.POST['maximum_num'],
            lecture_day=request.POST['lecture_day'],
            lecture_time=val5,
            lecture_room=request.POST['lecture_room'],
            create_date=timezone.now(),
        )
        subject.save()
        return redirect('CRS:index')
    else:
        form = SubjectForm()
    context = {'form': form}
    return render(request, 'CRS/subject_form.html', context)


def signup_list(request):
    """
    수강신청과목 리스트 출력
    """
    mysubject_count = Attendance.objects.select_related(
        'subject_code').filter(student_no_id=request.user.user_no)
    my_arr = []

    for list in mysubject_count:
        my_arr.append(list.subject_code.subject_code)

    subject_list = Subject.objects.exclude(
        subject_code__in=my_arr)  # 내가 신청한 수강신청내역 제외
    subject_count = Subject.objects.count()

    context = {'subject_list': subject_list,
               'subject_count': subject_count, 'mysubject_count': mysubject_count}
    return render(request, 'CRS/signup_list.html', context)


@csrf_exempt
def attendance_remove(request):
    """
    수업철회
    """
    if request.method == 'POST':
        user_id = request.user.user_no   # 세션에서 로그인한 유저의 번호 가져오기
        subject = Subject.objects.get(
            subject_code=request.POST['subject_code'])
        attendance = Attendance.objects.get(
            subject_code_id=subject, student_no_id=user_id)
        current_num = subject.current_num - 1
        subject.current_num = subject.current_num - 1

        if (current_num > subject.maximum_num):
            return JsonResponse({'result': 'fail'})
        else:
            with transaction.atomic():
                subject.save()
                attendance.delete()
            return JsonResponse({'result': 'success'})
    else:
        return render(request, 'CRS/singup_list.html')


@csrf_exempt
def attendance_create(request):
    """
    수업신청
    """
    if request.method == 'POST':
        user_id = request.user.user_no   # 세션에서 로그인한 유저의 번호 가져오기
        # 과목의 신청자수를 증가시키기 위해 과목 정보 가져오기
        subject = Subject.objects.get(
            subject_code=request.POST['subject_code'])
        current_num = subject.current_num + 1
        subject.current_num = subject.current_num + 1

        if (current_num > subject.maximum_num):      # 해당 과목의 인원이 초과되었으면 신청실패
            return JsonResponse({'result': 'fail'})
        else:
            attendance = Attendance(
                subject_code_id=request.POST['subject_code'],
                student_no_id=user_id,
            )
            with transaction.atomic():
                subject.save()
                attendance.save()
            return JsonResponse({'result': 'success'})
    else:
        return render(request, 'CRS/singup_list.html')
