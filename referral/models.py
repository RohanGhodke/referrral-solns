from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isEmployee = models.BooleanField(default=True)
    isSeeker = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class employeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    check_type = models.ForeignKey(role, on_delete=models.CASCADE)
    referral_id = models.CharField(max_length=20, primary_key=True)
    company = models.CharField(max_length=30)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' ' + self.referral_id


class jobPost(models.Model):
    job_title = models.CharField(max_length=20)
    experience_required = models.CharField(max_length=15)
    skillset_required = models.TextField()
    date_posted = models.DateField()
    job_place = models.CharField(max_length=40)
    job_description = models.TextField()
    employee = models.ForeignKey(employeeProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.user.first_name + ' ' + self.user.last_name + ' ' + self.job_title
 
    # @property
    # def delete(self):
    #     time_delta = 


class jobseekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    check_type = models.ForeignKey(role, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class jobApply(models.Model):
    jobpost_applied = models.ForeignKey(jobPost, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(jobseekerProfile, on_delete=models.CASCADE)
    date_applied = models.DateField()
    time_delta = models.DateField()

    def __str__(self):
        return self.jobseeker.user.first_name + ' ' + self.jobseeker.user.last_name + ' ' + self.jobpost_applied.job_title