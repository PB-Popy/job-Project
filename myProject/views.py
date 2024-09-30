from django.shortcuts import render,redirect
from django.http import HttpResponse
from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import Http404


def search(request):
    return render(request,'search.html')

@login_required
def jobfeedPage(request):
    data=jobModel.objects.all()
    context={
        'data':data
    }
    return render(request,'jobfeedPage.html',context) 


def addjobPage(request):
    curernt_user=request.user
    if request.method == 'POST':
        job=jobModel()

        job.user=curernt_user
        job.job_title=request.POST.get('job_title')
        job.company_name=request.POST.get('company_name')
        job.location=request.POST.get('location')
        job.salary=request.POST.get('salary')
        job.employment_type=request.POST.get('employment_type')
        job.posted_date=request.POST.get('posted_date')
        job.description=request.POST.get('description')
        job.save()
        messages.success(request,"Job created successfully")

        return redirect('jobfeedPage')
        
    return render(request,'addjobPage.html')

def viewjobPage(request,view_id):

    job = jobModel.objects.get(id=view_id)

    context={
        "job":job
    }

    return render(request,'Recruiter/viewjobPage.html',context)

def createdjob(request):
    curernt_user=request.user

    job=jobModel.objects.filter(user=curernt_user)

    context={
        "Job":job
    }

    return render(request,'Recruiter/createdjob.html',context)


def apply_now(request,apply_id):
    curernt_user=request.user
    if curernt_user.usertype == 'jobseeker':
        specific_job=jobModel.objects.get(id=apply_id)
        already_exists=jobApplyModel.objects.filter(user=curernt_user,job=specific_job).exists()

        context={
            'specific_job':specific_job,
            'already_exists':already_exists,
        }

        if request.method == 'POST':
            full_name=request.POST.get('full_name')
            work_experience=request.POST.get('work_experience')
            skills=request.POST.get('skills')
            linkedin_url=request.POST.get('linkedin_url')
            expected_salary=request.POST.get('expected_salary')
            resume=request.FILES.get('resume')
            cover=request.POST.get('cover')

            apply=jobApplyModel(
                user=curernt_user,
                job=specific_job,
                full_name=full_name,
                work_experience=work_experience,
                skills=skills,
                linkedin_url=linkedin_url,
                expected_salary=expected_salary,
                resume=resume,
                cover=cover,
            )
            apply.save()

            return redirect('jobfeedPage')


        return render(request,'seeker/apply_now.html',context)
    else:
        messages.warning(request,"You are not a job seeker")


def appliedjob(request):
    curernt_user=request.user

    job_applications=jobApplyModel.objects.filter(user=curernt_user)

    context = {
        "job":job_applications
    }

   
    return render(request,'seeker/appliedjob.html',context)

