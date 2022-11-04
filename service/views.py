from django.shortcuts import render
from django.shortcuts import redirect
from .forms import *
import hashlib
from django.shortcuts import get_object_or_404
from django.contrib import messages
import shortuuid


def home_page(request):
    form = CreateUrlForm()
    if request.method == 'POST':
        form = CreateUrlForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.short = shortuuid.ShortUUID().random(length=16)
            url.save()
            print("short: "+url.short)
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'service/home.html', context)


def rdr(request, url):
    url_object = get_object_or_404(Url, short=url)
    return redirect(url_object.long)
