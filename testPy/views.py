from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
# from django.contrib.auth.views import password_reset
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from datetime import date, datetime
from eligibility.models import Quote
import pytz
import random


def login_view(request):
    if request.user.is_authenticated:
        return redirect('landing_page')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        next_url = request.POST.get('next', '')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                ##                if user.last_login is None or user.last_login <\
                ##                   datetime(year=2017, month=3, day=3, hour=15,
                ##                            minute=5, tzinfo=pytz.timezone('Africa/Accra')):
                ##                    login(request, user)
                ##                    return redirect('change_password')
                login(request, user)

                if next_url == '':
                    return redirect('landing_page')
                else:
                    print(next_url)
                    return redirect(next_url)
            else:
                login_failed = True
    else:
        form = AuthenticationForm()

    context = {}
    context['form'] = form
    return render(request, 'login_page.html', context)


@login_required
def change_password_view(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            logout(request)
            return redirect('login')
    else:
        form = PasswordChangeForm(user)

    context = {}
    context['form'] = form
    return render(request, 'change_password.html', context)


@login_required
def landing_page_view(request):
    quote = ''
    current_time = datetime.now()
    if current_time.hour < 12:
        greeting = "Good Morning"
    elif current_time.hour >= 12 and current_time.hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    quotes = Quote.objects.all()
    if quotes:
        quote = quotes[random.randint(0, quotes.count() - 1)]
    context = {}
    context['greeting'] = greeting
    context['quote'] = quote
    return render(request, 'landing_page.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def http403_view(request):
    response = render_to_response('403.html', context=RequestContext(request))
    response.status_code = 403
    return response


def http404_view(request):
    response = render_to_response('404.html', context=RequestContext(request))
    response.status_code = 404
    return response


def http500_view(request):
    response = render_to_response('500.html', context=RequestContext(request))
    response.status_code = 500
    return response
