from django.contrib import admin
from .models import Games, Tags

# Register your models here.
@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    pass


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass