from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
from django.shortcuts import get_object_or_404
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import F


@login_required(login_url='login')
def create_short(request):
    form = CreateUrlForm()
    links = Url.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CreateUrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.user = request.user
            url.save()
            url = form.save()
            url.is_expired()
            url.generate_short_url()

    context = {
        'links': links,
        'form': form,
    }
    return render(request, 'service/home.html', context)


def page_redirect(request, url):
    url_object = get_object_or_404(Url, short=url)
    context = {}
    if url_object.active is True and url_object.click_current < url_object.click_limit:
        url_object.increment_click_current()
        response = redirect(url_object.long)
        response.status_code = 307
        return response
    else:

        return render(request, 'service/not_found.html', context)


def register_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'service/register_user.html', context)


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="service/login_user.html", context={"login_form": form})


def logout_user(request):
    """ Log outs user"""
    logout(request)
    return redirect('login')


def delete_url(request, url):
    """Deletes url specified with request"""
    url = Url.objects.get(short=url)
    if request.method == "POST":
        url.delete()
        return redirect('/')
    context = {}
    return render(request, 'service/home.html', context)


def toggle_url(request, url):
    """Toggles status of url specified with request"""
    url = Url.objects.get(short=url)
    if request.method == "POST":
        url.toggle_active()
        return redirect('/')
    context = {}
    return render(request, 'service/home.html', context)


def change_expiration_time(request, url):
    """Changes expiration date of url specified in request"""
    url = Url.objects.get(short=url)
    form = ModifyUrlForm(instance=url)

    if request.method == 'POST':
        form = ModifyUrlForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'service/home.html', context)
