from django.shortcuts import render,redirect
from django.http import HttpResponse
from myApp.models import *
from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import Http404

def jobfeedPage(request):
    data=jobModel.objects.all()
    context={
        'data':data
    }
    return render(request,'jobfeedPage.html',context) 

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        if not username or not password:
            messages.warning(request,'Both username and password are required')
            return render(request,'loginPage.html')
        
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Login successfully')
            return redirect('jobfeedPage')
        else:
            messages.warning(request,'Invalid username or password')
        
    return render(request,'loginPage.html') 

def signupPage(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        email=request.POST.get("email")
        usertype=request.POST.get("usertype")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        if not all([username,email,usertype,password,confirm_password]):
            messages.warning(request,'All fields are required')
            return render(request,'signupPage.html')
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request,'Invalid email format')
            return render(request,'signupPage.html')
        
        if password != confirm_password:
            messages.warning(request,'Password did not match')
            return render(request,'signupPage.html')
        
        if len(password) < 8:
            messages.warning(request,'Password must be at least 8 characters long')
            return render(request,'signupPage.html')
        
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(request,'Password must contain both letters and numbers')
            return render(request,'signupPage.html')
        
        try:
            user=custom_user.objects.create_user(
                username=username,
                email=email,
                usertype=usertype,
                password=password,
            )
            messages.success(request,'Account created successfully!Please login...')
            return redirect('loginPage')
        
        except IntegrityError:
            messages.warning(request,'username or email already exists!')
            return render(request,'signupPage.html')
        
    return render(request,'signupPage.html') 

def logoutPage(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("loginPage")

def addjobPage(request):
    curernt_user=request.user

    if curernt_user.usertype == 'recruiter':
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
    else:
        messages.warning(request,"You are not a recruiter")

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




