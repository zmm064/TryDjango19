from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        # 只有通过这个返回的user才能实现登录功能
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse('posts:list'))

    return render(request, "form.html", {"form":form, "title":title})


def logout_view(request):
    logout(request)
    return render(request, "form.html")


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return redirect(reverse('account:login'))


    return render(request, "form.html", {"title":title, "form":form})