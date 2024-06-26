"""Organizing and managing view functions in entry application."""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm


def home(request):
    """
    View function for displaying the homepage.

    Parameters:
    - request: HttpRequest object representing the current request.
               Contains metadata about the request, such as headers and body content.

    Returns:
    - Rendered response containing the homepage content.
    """
    is_main_page = request.path == '/'  # Assuming the main page URL is '/'
    return render(request, 'entry/startpage.html',
                  {'is_main_page': is_main_page, 'user': request.user})


def register(request):
    """
    View function for user registration process.

    Parameters:
    - request: HttpRequest object representing the current request.
               Contains metadata about the request, such as headers and body content.

    Returns:
    - If the request method is POST and the form is valid, it saves the user's registration data,
      displays a success message, and redirects to the login page.
    - If the request method is GET, it renders the registration form.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created for {form.cleaned_data["username"]}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'entry/register.html', context=context)


def login(request):
    """
    View function for user login process.

    Parameters:
    - request: HttpRequest object representing the current request.
               Contains metadata about the request, such as headers and body content.

    Returns:
    - If the req_method is POST and the login form is valid, it attempts to authenticate the user,
      displays a success message, logs in the user, and redirects to the profile page.
    - If the request method is GET, it renders the login form.
    """
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            messages.success(request, f'{form.cleaned_data["username"]} successfully logged in')
            if user is not None:
                auth.login(request, user)
                return redirect('profile')
    context = {'form': form}
    return render(request, 'entry/login.html', context=context)


def logout(request):
    """
    View function for logging out a user.

    Parameters:
    - request: HttpRequest object representing the current request.
               Contains metadata about the request, such as headers and body content.

    Returns:
    - Redirects the user to the login page after logging them out.
    """
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    """
    View function for displaying user profile.

    Parameters:
    - request: HttpRequest object representing the current request.
               Contains metadata about the request, such as headers and body content.

    Returns:
    - Rendered response containing the user profile page.
    """
    return render(request, 'entry/startpage.html')
