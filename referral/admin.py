from django.contrib import admin
from .models import role, employeeProfile, jobPost, jobseekerProfile, jobApply

# Register your models here.
admin.site.register(role)
admin.site.register(employeeProfile)
admin.site.register(jobseekerProfile)
admin.site.register(jobPost)
admin.site.register(jobApply)