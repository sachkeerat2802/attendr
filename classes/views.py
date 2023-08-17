import json
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Class, Lecture, Attendance
from django.http import JsonResponse, FileResponse
from users.models import StaffProfile, UserProfile
from django.views.decorators.csrf import csrf_exempt
from .forms import ClassForm, LectureForm, AttendanceForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import detect_id, generate_lecture_report, generate_class_report


@login_required(login_url="login")
def view_all_classes(request):

    user = request.user
    if user.is_staff == True:
        profile = StaffProfile.objects.get(empno=user.uid)
        classes = Class.objects.filter(profile=profile)
    else:
        profile = UserProfile.objects.get(prn=user.uid)
        classes = Class.objects.all()

    context = {'classes': classes, 'profile': profile}
    return render(request, 'classes/classes.html', context)


@login_required(login_url="login")
def view_class(request, pk):

    user = request.user
    class_obj = Class.objects.get(id=pk)
    lectures = Lecture.objects.filter(class_object=class_obj)
    count = {'lectures': len(Lecture.objects.filter(class_object=class_obj)), 'users': len(
        Class.objects.get(id=pk).users.all())}

    if user.is_staff == True:
        profile = StaffProfile.objects.get(empno=user.uid)
    else:
        profile = UserProfile.objects.get(prn=user.uid)

    if profile not in class_obj.users.all() and profile != class_obj.profile:
        return redirect('classes')

    if request.method == "POST":
        form_type = request.POST.get('form-type')

        if form_type == "add-member":
            try:
                student = request.POST['prn']
                student_profile = UserProfile.objects.get(prn=student)
                class_obj.users.add(student_profile)
                return redirect('class', pk=class_obj.id)
            except:
                messages.error(request, "User does not exist!")

        elif form_type == "generate-report":
            output = generate_class_report(class_obj, lectures)
            response = FileResponse(
                output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={class_obj.name}_AttendanceReport.xlsx'

            return response

    context = {'class_obj': class_obj,
               'profile': profile, 'lectures': lectures, 'count': count}
    return render(request, 'classes/class.html', context)


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def create_class(request):

    user = request.user
    profile = StaffProfile.objects.get(empno=user.uid)
    form = ClassForm()

    if request.method == "POST":
        form = ClassForm(request.POST, request.FILES)

        if form.is_valid():
            class_obj = form.save(commit=False)
            class_obj.profile = profile
            class_obj.save()
            return redirect('classes')

    context = {'form': form, 'profile': profile}
    return render(request, 'classes/create_class.html', context)


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def edit_class(request, pk):

    class_obj = Class.objects.get(id=pk)
    form = ClassForm(instance=class_obj)
    profile = StaffProfile.objects.get(empno=request.user.uid)

    if profile != class_obj.profile:
        return redirect('classes')

    if request.method == "POST":
        form = ClassForm(request.POST, request.FILES, instance=class_obj)

        if form.is_valid:
            form.save()
            return redirect('class', pk=class_obj.id)

    context = {'form': form, 'class_obj': class_obj, 'profile': profile}
    return render(request, 'classes/edit_class.html', context)


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def delete_class(request, pk):

    class_obj = Class.objects.get(id=pk)
    profile = StaffProfile.objects.get(empno=request.user.uid)

    if profile != class_obj.profile:
        return redirect('classes')

    if request.method == "POST":
        class_obj.delete()
        return redirect('classes')

    context = {'class_obj': class_obj, 'profile': profile}
    return render(request, 'classes/delete_class.html', context)


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def remove_member(request, pk, prn):

    try:
        class_obj = Class.objects.get(id=pk)
        profile = UserProfile.objects.get(prn=prn)
    except:
        messages.error(request, 'Class ID or PRN is wrong!')

    if request.method == "POST":
        class_obj.users.remove(profile)
        return redirect('class', pk=class_obj.id)

    context = {'class_obj': class_obj, 'profile': profile}
    return render(request, 'classes/remove_member.html', context)


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def create_lecture(request, pk):

    form = LectureForm()
    class_obj = Class.objects.get(id=pk)
    profile = StaffProfile.objects.get(empno=request.user.uid)

    if profile != class_obj.profile:
        return redirect('classes')

    if request.method == "POST":
        form = LectureForm(request.POST)

        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.class_object = class_obj

            if Lecture.objects.filter(class_object=class_obj, no=lecture.no).exists():
                messages.error(request, "Lecture with this no. already exists")

            else:
                lecture.save()

                for user in class_obj.users.all():
                    log = Attendance.objects.create(
                        class_object=class_obj, profile=user, lecture=lecture)
                    log.save()

                return redirect('class', pk=pk)

    context = {'form': form, 'class_obj': class_obj, 'profile': profile}
    return render(request, 'classes/create_lecture.html', context)


@login_required(login_url="login")
def view_lecture(request, pk, no):

    user = request.user
    if user.is_staff == True:
        profile = StaffProfile.objects.get(user=user)
    else:
        profile = UserProfile.objects.get(user=user)

    class_obj = Class.objects.get(id=pk)
    lecture = Lecture.objects.get(class_object=class_obj, no=no)
    attendances = Attendance.objects.filter(lecture=lecture)
    times = {'start': lecture.start_time.strftime(
        '%I:%M %p'), 'end': lecture.end_time.strftime('%I:%M %p')}

    if request.method == "POST":
        output = generate_lecture_report(class_obj, lecture)
        response = FileResponse(
            output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={class_obj.name}_Lecture{lecture.no}_AttendanceReport.xlsx'

        return response

    context = {'lecture': lecture, 'class_obj': class_obj,
               'attendances': attendances, 'profile': profile, 'times': times}
    return render(request, 'classes/lecture.html', context)


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def delete_lecture(request, pk, no):

    class_obj = Class.objects.get(id=pk)
    profile = StaffProfile.objects.get(empno=request.user.uid)
    lecture = Lecture.objects.get(class_object=class_obj, no=no)

    if profile != class_obj.profile:
        return redirect('classes')

    if request.method == "POST":
        lecture.delete()
        return redirect('class', pk=pk)

    context = {'class_obj': class_obj, 'lecture': lecture}
    return render(request, 'classes/delete_lecture.html', context)


@csrf_exempt
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def detect_attendance(request, pk, no):

    class_obj = Class.objects.get(id=pk)
    lecture = Lecture.objects.get(class_object=class_obj, no=no)
    profile = StaffProfile.objects.get(empno=request.user.uid)
    context = {'lecture': lecture, 'class_obj': class_obj, 'profile': profile}

    if request.method == "POST":
        data = json.loads(request.body)
        response = detect_id(class_obj, lecture, data)
        try:
            if "info" in response:
                return JsonResponse({'info': f"{response['info']}"})
            elif "success" in response:
                return JsonResponse({'success': f"{response['success']}"})
        except:
            pass

    return render(request, 'classes/detect_attendance.html', context)


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_staff, login_url="index")
def edit_attendance(request, pk, no, prn):

    class_obj = Class.objects.get(id=pk)
    lecture = Lecture.objects.get(class_object=class_obj, no=no)
    staff_profile = StaffProfile.objects.get(empno=request.user.uid)
    profile = UserProfile.objects.get(prn=prn)
    log = Attendance.objects.get(profile=profile, lecture=lecture)
    form = AttendanceForm(instance=log)

    if staff_profile != class_obj.profile:
        return redirect('classes')

    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=log)

        if form.is_valid:
            form.save()
            return redirect('lecture', pk=class_obj.id, no=lecture.no)

    context = {'class_obj': class_obj, 'lecture': lecture,
               'profile': profile, 'form': form}
    return render(request, 'classes/edit_attendance.html', context)
