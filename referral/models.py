from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class employeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_id = models.CharField(max_length=20, primary_key=True)
    company = models.CharField(max_length=30)

    def __str__(self):
        return self.referral_id


class jobPost(models.Model):
    job_title = models.CharField(max_length=20)
    experience_required = models.CharField(max_length=15)
    skillset_required = models.TextField()
    date_posted = models.DateField()
    job_place = models.CharField(max_length=40)
    job_description = models.TextField()
    employee = models.ForeignKey(employeeProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title
