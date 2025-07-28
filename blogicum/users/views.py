from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse


def registration(request):
    return render(request, 'registration/registration_form.html')


def logout_user(request):
    logout(request)
    return redirect(reverse('blog:index'))
