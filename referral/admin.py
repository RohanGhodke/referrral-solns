from django.contrib import admin
from .models import employeeProfile, jobPost

# Register your models here.
admin.site.register(employeeProfile)
admin.site.register(jobPost)