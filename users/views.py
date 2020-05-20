from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm

# Create your views here.

# 편의상 main => movies:index로 통일
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # main화면으로 돌아가기
            return redirect('movies:index')

    form = UserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'auth/signup.html', context)

def signin(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 메인화면으로 로그인한 상태로 돌아가기
            return redirect('movies:index')

    form = AuthenticationForm()
    context = {
        'form':form, 
    }
    return render(request, 'auth/signin.html', context)

@login_required
def signout(request):
    logout(request)
    # 메인화면으로 돌아가기
    return redirect('movies:index')