from .models import User
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .forms import RegisterUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


def login_user(request):

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "The email does not exist!")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or Password is incorrect!")

    return render(request, 'authentication/login.html')


@login_required(login_url='login')
def logout_user(request):

    if request.method == "POST":
        logout(request)
        return redirect('index')

    return render(request, 'authentication/logout.html')


def register_user(request):

    form = RegisterUserCreationForm()
    if request.method == "POST":
        form = RegisterUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # if user.email.split("@")[1] == "sicsr.ac.in":
            user.save()

            subject = "Welcome to Attendr"
            message = f"You have registered on Attendr! Your credentials are mentioned below:\n\nEMAIL: {user.email}\nPRN: {user.uid}\n\nPlease set your password by clicking http://127.0.0.1:8000/password/set/!"

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return redirect('check_mail')

            # else:
            #     messages.error(request, "Email doesn't belong to SICSR!")
        else:
            messages.error(request, "Form is invalid!")

    context = {'form': form}
    return render(request, 'authentication/register.html', context)


def check_mail(request):
    return render(request, 'authentication/check_mail.html')
