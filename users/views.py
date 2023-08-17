from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import UserProfile, StaffProfile, User
from .forms import UserProfileForm, StaffProfileForm
from authentication.forms import RegisterStaffCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser, login_url="index")
def add_user(request):

    profile = StaffProfile.objects.get(user=request.user)

    form = RegisterStaffCreationForm()
    if request.method == "POST":
        form = RegisterStaffCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()

            subject = "Welcome to Attendr"
            message = f"You have been registered on Attendr by an administrator of your organization! Your login credentials are mentioned below:\n\nEMAIL: {user.email}\nEMPLOYEE NO: {user.uid}\n\nPlease set your password by clicking http://127.0.0.1:8000/password/set/!"

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect("add_user")

        else:
            messages.add_message(request, messages.ERROR, "Form is invalid!")

    context = {'form': form, 'profile': profile}
    return render(request, 'users/add_user.html', context)


@ login_required(login_url='login')
def view_user(request, pk):

    user = User.objects.get(uid=pk)
    if user.is_staff == True:
        profile = StaffProfile.objects.get(empno=pk)
    else:
        profile = UserProfile.objects.get(prn=pk)

    context = {'profile': profile, 'user': user}
    return render(request, 'users/user.html', context)


@ login_required(login_url='login')
def edit_user(request, pk):

    user = request.user
    if user.is_staff == True:
        profile = StaffProfile.objects.get(user=user)
        form = StaffProfileForm(instance=profile)
    else:
        profile = UserProfile.objects.get(user=user)
        form = UserProfileForm(instance=profile)

    if request.method == "POST":
        if user.is_staff == True:
            profile = StaffProfile.objects.get(user=user)
            form = StaffProfileForm(
                request.POST, request.FILES, instance=profile)
        else:
            profile = UserProfile.objects.get(user=user)
            form = UserProfileForm(
                request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('user', pk=user.uid)

    context = {'form': form, 'profile': profile}
    return render(request, 'users/edit_user.html', context)
