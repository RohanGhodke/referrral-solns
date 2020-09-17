from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import employeeProfile, jobPost

# Create your views here.


def index(request):
    return render(request, 'index.html')


def employeeSignup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        referral_id = request.POST.get('referral')
        company = request.POST.get('company')

        myUser = User.objects.create_user(username, email, password)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()

        profile_data = employeeProfile(
            user=myUser, referral_id=referral_id, company=company)
        profile_data.save()

        return redirect('login')

    return render(request, 'signup.html')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')

        user = authenticate(username=loginusername, password=loginpassword)

        if user:
            if user.is_active:
                login(request, user)
                print('1')
                return redirect('index')
            else:
                return redirect('index')
        else:
            return HttpResponse("Invalid login details given")  
    else:
        return render(request, 'login.html')


def handleLogout(request):
    logout(request)
    return redirect('index')


def job_post(request):
    if request.method == 'POST':
        job_title = request.POST.get('title')
        experience_required = request.POST.get('experience_required')
        skillset_required = request.POST.get('skillset_required')
        date_posted = request.POST.get('date')
        job_place = request.POST.get('place')
        job_description = request.POST.get('job_description')

        if request.user.is_authenticated:
            user = request.user
            myEmployee = employeeProfile.objects.get(user=user)
            post = jobPost(job_title=job_title, experience_required=experience_required, skillset_required=skillset_required,
                           date_posted=date_posted, job_place=job_place, job_description=job_description, employee=myEmployee)
            post.save()

            # profile_data = employeeProfile.objects.get(user=user)
            # profile_data.posts.add(post)

        return HttpResponse('job posted')
    # else:
    #     return HttpResponse('404-Page Not Found')
    return render(request, 'jobpost.html')


def joblist(request):
    data = jobPost.objects.all()
    context = {'data': data}
    return render(request, 'joblisting.html', context)


def jobapply(request):
    return render(request, 'jobapply.html')

