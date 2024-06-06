from django import forms
from core.models import Groups

class CreateGroupForm(forms.ModelForm):

    class Meta:
        model = Groups
        fields = ("name", "group_size", "is_public", "game")
