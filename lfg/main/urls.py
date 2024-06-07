from django.contrib import admin
from django.urls import path
from .views import ExploreView, CreateGroupView, FindGroupView, JoinGroupView, GroupView

app_name = 'main' 

urlpatterns = [
    path("", ExploreView.as_view(), name="explore"),
    path("create", CreateGroupView.as_view(), name="create_group"),
    path("find", FindGroupView.as_view(), name="find_group"),
    path("join/<int:group_id>", JoinGroupView.as_view(), name="join_group"),
    path("group/<int:group_id>", GroupView.as_view(), name="group")

]
