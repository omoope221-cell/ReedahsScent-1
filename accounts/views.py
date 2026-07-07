from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('store:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
