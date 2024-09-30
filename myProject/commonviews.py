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

from django.contrib.auth.hashers import check_password

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

@login_required
def changepassword(request):

    current_user=request.user

    if request.method == 'POST':
        current_password=request.POST.get('current_password')
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')

        if check_password(current_password,request.user.password):

            if new_password==confirm_password:

                current_user.set_password(new_password)

                current_user.save()

                messages.success(request,'Password changed successfully')
      

    return render(request,'changepassword.html')