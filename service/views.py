import time
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from .forms import UserCreationForm
from .utils import get_ip, get_referer


def timer(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        start = time.time()
        result = func(request, *args, **kwargs)
        clicks = get_object_or_404(
            Url, short_url=kwargs['short_url']).click_set.all()
        click = clicks.latest('created_at')
        duration = (time.time() - start) * 1000
        click.save_redirect_time(duration)
        return result
    return wrapper


def home(request):
    if request.user.is_authenticated:
        create_url_form = CreateUrlForm()
        urls = Url.objects.filter(user=request.user)
        if request.method == 'POST':
            url_creation_form = CreateUrlForm(request.POST)
            if url_creation_form.is_valid():
                url = url_creation_form.save(commit=False)
                url.user = request.user
                url.save()
                url.is_expired()
                url.generate_short_url_base58()
        context = {
            'user': request.user,
            'urls': urls,
            'create_url_form': create_url_form,
        }
        return render(request, 'service/home.html', context)
    else:
        create_url_form = CreateUrlForm()
        if request.method == 'POST':
            url_creation_form = CreateUrlForm(request.POST)
            if url_creation_form.is_valid():
                url = url_creation_form.save(commit=False)

                url.save()
                url.is_expired()
                url.generate_short_url_base58()
                messages.info(request, "Your new short url: ")
                messages.info(
                    request, "http://127.0.0.1:8000/r/"+url.short_url)

        context = {
            'user': request.user,
            'create_url_form': create_url_form,
        }
        return render(request, 'service/home.html', context)


@timer
def page_redirect(request, short_url):
    url_object = get_object_or_404(Url, short_url=short_url)
    if url_object.active is not True:
        context = {'message': 'Url is deactivated'}
        return render(request, 'service/not_found.html', context)
    elif url_object.get_number_of_clicks() >= url_object.click_limit:
        context = {'message': 'Click limit has been reached'}
        return render(request, 'service/not_found.html', context)
    elif url_object.expiration_time < timezone.now():
        context = {'message': 'Link has expired'}
        return render(request, 'service/not_found.html', context)
    else:
        referer = get_referer(request)
        ip = get_ip(request)
        click = Click()
        click.save(url_object, referer, ip)
        response = redirect(url_object.long_url)
        response.status_code = 307
        return response


def register_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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


@login_required(login_url='login')
def delete_url(request, short_url):
    """Deletes url specified with request"""
    url = Url.objects.get(short_url=short_url)
    if request.method == "POST":
        url.delete()
        messages.info(request, 'Link has been deleted')
        return redirect('/')
    context = {}
    return render(request, 'service/home.html', context)


@login_required(login_url='login')
def toggle_url(request, short_url):
    """Toggles status of url specified with request"""
    url = Url.objects.get(short_url=short_url)
    if request.method == "POST":
        url.toggle_active()
        messages.info(request, 'Link status has been changed')
        return redirect('/')
    context = {}
    return render(request, 'service/home.html', context)


@login_required(login_url='login')
def change_expiration_time(request, short_url):
    """Changes expiration date of url specified in request"""
    url = Url.objects.get(short_url=short_url)
    form = UpdateExpirationUrlForm(instance=url)
    if request.method == 'POST':
        form = UpdateExpirationUrlForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            messages.info(request, 'Date has been changed')
            return redirect('/')
    context = {'form': form}
    return render(request, 'service/home.html', context)


@login_required(login_url='login')
def info_page(request, short_url):
    clicks = get_object_or_404(Url, short_url=short_url).click_set.all()
    context = {'clicks': clicks}
    return render(request, 'service/info.html', context)
