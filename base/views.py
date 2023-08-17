from .models import TimeTable
from classes.models import Class, Attendance, Lecture
from django.shortcuts import render, redirect
from users.models import UserProfile, StaffProfile
from users.models import UserProfile, StaffProfile
from django.contrib.auth.decorators import login_required


def index(request):

    if request.user.is_authenticated:
        user = request.user
        if user.is_staff == True:
            profile = StaffProfile.objects.get(user=user)
        else:
            profile = UserProfile.objects.get(user=user)
        name = profile.name.split(" ")[0]

        if request.user.is_staff != True:
            class_statistics = []
            user_statistics = {'classes': 0, 'total': 0,
                               'present': 0, 'absent': 0, 'percentage': 0}

            try:
                classes = Class.objects.all()
                for class_obj in classes:
                    if profile in class_obj.users.all():
                        user_statistics['classes'] += 1

                        temp = {"name": "", "total": 0, "present": 0,
                                "absent": 0, "percentage": 0}
                        temp['name'] = class_obj.name

                        logs = Attendance.objects.filter(
                            class_object=class_obj, profile=profile)
                        temp['total'] = len(logs)

                        if temp['total'] > 0:
                            for log in logs:
                                if log.value == "P":
                                    temp['present'] += 1
                                    user_statistics['present'] += 1
                                else:
                                    temp['absent'] += 1
                                    user_statistics['absent'] += 1

                            temp['percentage'] = round((
                                temp['present'] / temp['total']) * 100, 1)

                        class_statistics.append(temp)

                if len(classes) > 0:
                    user_statistics['total'] = user_statistics['present'] + \
                        user_statistics['absent']
                    user_statistics['percentage'] = round((
                        user_statistics['present'] / user_statistics['total']) * 100, 1)

            except:
                pass

            context = {'profile': profile,
                       'user_stats': user_statistics, 'class_stats': class_statistics, 'name': name}
            return render(request, 'base/dashboard.html', context)

        else:

            classes = Class.objects.filter(profile=profile)
            class_statistics = []
            staff_stats = {'classes': 0,
                           'lectures': 0, 'students': 0}
            staff_stats['classes'] = len(classes)

            for class_obj in classes:
                temp = {'name': "", 'lectures': 0, 'students': 0}
                temp['name'] = class_obj.name
                staff_stats['lectures'] += len(Lecture.objects.filter(
                    class_object=class_obj))
                temp['lectures'] = len(Lecture.objects.filter(
                    class_object=class_obj))
                staff_stats['students'] += len(class_obj.users.all())
                temp['students'] = len(class_obj.users.all())
                class_statistics.append(temp)

            context = {'profile': profile, 'name': name,
                       'staff_stats': staff_stats, 'class_stats': class_statistics}
            return render(request, 'base/dashboard.html', context)

    else:
        return render(request, 'base/index.html')


@ login_required(login_url='login')
def view_timetable(request):

    user = request.user
    if user.is_staff == True:
        profile = StaffProfile.objects.get(user=user)
    else:
        profile = UserProfile.objects.get(user=user)

    if request.method == "POST":
        form_type = request.POST.get('form-type')

        if form_type == "add-tt":
            name = request.POST['name']
            timetable_obj = TimeTable.objects.create(name=name, user=user)
            timetable_obj.save()
            return redirect('timetable')

        else:
            name = request.POST['removed']
            timetable_obj = TimeTable.objects.get(name=name, user=user)
            timetable_obj.delete()
            return redirect('timetable')

    classes = TimeTable.objects.filter(user=user)
    context = {'classes': classes, 'profile': profile}
    return render(request, 'base/timetable.html', context)
