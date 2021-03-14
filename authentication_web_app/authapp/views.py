from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required()
def dashboard_view(request):
    return render(request, 'dashboard.html')


def signup_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account Created Successfully')
                return redirect('login')

        context = {'form': form}
        return render(request, 'signup.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Incorrect username or password')

        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')