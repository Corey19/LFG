from django.contrib import admin
from django.urls import path
from .views import CreateUserView, LoginView, LogoutView

app_name = 'user' 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", CreateUserView.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login_user"),
    path("logout/", LogoutView.as_view(), name="logout_user")
]
