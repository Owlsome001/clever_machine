

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('skills', views.skills, name="skills"),
    path('teaching', views.teaching, name="teaching"),
    path('download-skill', views.downloadModel, name="dowload-skill"),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_request, name="logout"),
    path('accounts/login/',views.login_request, name="login"),
    path('projects',views.get_projects_by_user, name="projects"),
    path('projects/<int:id>/',views.edit_project, name="projects")

    # get_projects_by_user

]
