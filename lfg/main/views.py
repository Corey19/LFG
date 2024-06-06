from django.shortcuts import render, redirect
from django.views.generic import View
from core.models import Games, Groups
from .forms import CreateGroupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


class ExploreView(LoginRequiredMixin, View):
    def get(self, request):
        games = Games.objects.all()
        return render(request, "main/explore.html", {"games": games})
    def post(self, request):
        pass


class CreateGroupView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateGroupForm()
        return render(request, "main/create_group.html", {"form": form})

    def post(self, request):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            user = request.user  
            group.members.add(user)
            return redirect("main:explore")
        return render(request, "main/create_group.html", {"form": form})
    

class FindGroupView(LoginRequiredMixin, View):
    def get(self, request):
        groups = Groups.objects.all()
        return render(request, "main/find_group.html", {"groups": groups})

    def post(self, request):
        pass


class JoinGroupView(LoginRequiredMixin, View):
    def get(self, request, group_id):
        group = Groups.objects.get(pk=group_id)
        if request.user.is_authenticated is False:
            return redirect("user:login_user")
        if group is not None and request.user not in group.members.all():
            try:
                groups = Groups.objects.filter(members=request.user)
                if len(groups) == 0:
                    group.members.add(request.user)
            except Groups.DoesNotExist:
                group.members.add(request.user)
            
            
            return redirect("main:find_group")
        return redirect("main:find_group")