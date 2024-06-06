from django.contrib import admin
from .models import Games

# Register your models here.
@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    pass