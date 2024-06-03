from django.shortcuts import render, redirect
from django.views import View
from .forms import MyUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "user/login.html", {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to success URL (e.g., protected view)
                return
            else:
                # Handle invalid login attempt (e.g., display error message)
                form.add_error(None, 'Invalid username or password')

        return render(request, 'user/login.html', {"form": form})


class CreateUserView(View):
    
    def get(self, request):
        form = MyUserCreationForm()
        return render(request, "user/register.html", {"form": form})

    def post(self, request):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user:login_user")
        return render(request, "user/register.html", {"form": form})

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request) 
        return redirect('user:login_user') 