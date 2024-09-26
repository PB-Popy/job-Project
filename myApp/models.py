from django.db import models
from django.contrib.auth.models import AbstractUser

class custom_user(AbstractUser):
    USER={
        ('recruiter','Recruiter'),
        ('jobseeker','Jobseeker')
    }
    usertype=models.CharField(choices=USER,max_length=100,null=True)
    profile_pic=models.ImageField(upload_to='media/profile_pic',null=True)

    def __str__(self):
        return self.username
    

class jobModel(models.Model):
    Job_Type={
        ('full_time','Full_time'),
        ('part_time','Part_time'),
    }
    user=models.ForeignKey(custom_user,null=True,blank=True,on_delete=models.CASCADE)
    job_title=models.CharField(max_length=100,null=True,blank=True)
    company_name=models.CharField(max_length=100,null=True,blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    salary=models.PositiveIntegerField(null=True,blank=True)
    employment_type=models.CharField(max_length=50,choices=Job_Type,null=True,blank=True)
    posted_date=models.DateTimeField(auto_now_add=True)
    application_deadline=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.job_title}at{self.company_name}"
    
class jobApplyModel(models.Model):
    user=models.ForeignKey(custom_user,null=True,blank=True,on_delete=models.CASCADE)
    job=models.ForeignKey(jobModel,on_delete=models.CASCADE,null=True,blank=True)
    resume=models.FileField(upload_to='media/resume',max_length=200,null=True,blank=True)
    cover=models.TextField(null=True,blank=True)
    full_name=models.CharField(max_length=100,null=True,blank=True)
    work_experience=models.CharField(max_length=100,null=True,blank=True)
    skills=models.CharField(max_length=100,null=True,blank=True)
    linkedin_url=models.URLField(max_length=100,null=True,blank=True)
    expected_salary=models.PositiveIntegerField(null=True,blank=True)
   
   