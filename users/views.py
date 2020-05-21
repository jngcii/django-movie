from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# Create your views here.

# 편의상 main => index로 통일
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # main화면으로 돌아가기
            return redirect('home')

    form = CustomUserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'users/signup.html', context)

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 메인화면으로 로그인한 상태로 돌아가기
            return redirect('home')

    form = AuthenticationForm()
    context = {
        'form':form, 
    }
    return render(request, 'users/signin.html', context)

@login_required
def signout(request):
    logout(request)
    # 메인화면으로 돌아가기
    return redirect('home')