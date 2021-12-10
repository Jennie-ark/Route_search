from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegistrationForm

__all__ = (
    'login_view', 'logout_view', 'register_view'
)


def login_view(request):
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        _next = _next or '/'
        return redirect(_next)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создает нового пользователя, но пока не сохраняет в базу данных.
            new_user = user_form.save(commit=False)
            # Задает пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняет пользователя в базе данных.
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        return render(request, 'accounts/register.html', {'form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': user_form})
