from django.contrib import admin
from . models import Project

admin.site.site_header =" Clever Computer"
admin.site.site_title =" Clever Computer"
admin.site.index_title =" Welcome Admin"
# Register your models here.
admin.site.register(Project)
# admin.site.register(User)
