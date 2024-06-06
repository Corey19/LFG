from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import MyUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "user/login.html", {"form": form})
    
    def post(self, request):
        print(request.user)
        if request.user.is_authenticated:
            return redirect("main:find_group")
        form = AuthenticationForm(None, data=request.POST)
        if form.is_valid():
            print("valid")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # Redirect to success URL (e.g., protected view)
                return redirect("main:find_group")
            else:
                # Handle invalid login attempt (e.g., display error message)
                form.add_error(None, 'Invalid username or password')
        else:
            # Handle form validation errors
            print("Form validation errors:")  # Optional for debugging
            for error in form.errors:
                print(error)  # Optional for debugging

        return render(request, "user/login.html", {"form": form})


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
        logout(request) 
        return redirect('user:login_user') 