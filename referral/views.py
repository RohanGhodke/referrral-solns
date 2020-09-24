from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import employeeProfile, jobPost, jobseekerProfile, jobApply, role
import datetime
import smtplib

# Create your views here.


def index(request):
    tday = datetime.date.today()
    time_delta = tday + datetime.timedelta(days=30)
    print(time_delta)
    if request.user.is_authenticated:
        user = request.user
        data = role.objects.get(user=user)
        context = {'data': data}
        return render(request, 'index.html', context)
    else:
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

        role_data = role(user=myUser)
        role_data.save()

        profile_data = employeeProfile(
            user=myUser, check_type=role_data, referral_id=referral_id, company=company)
        profile_data.save()

        return redirect('login')
    else:
        return render(request, 'signup.html')


def seekerSignup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        contact = request.POST.get('contact')

        myUser = User.objects.create_user(username, email, password)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.save()

        isSeeker = True
        isEmployee = False

        role_data = role(user=myUser, isEmployee=isEmployee, isSeeker=isSeeker)
        role_data.save()

        profile_data = jobseekerProfile(user=myUser, check_type=role_data, contact=contact)
        profile_data.save()

        return redirect('login')
    else:
        return render(request, 'seekerSignup.html')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername')
        loginpassword = request.POST.get('loginpassword')

        user = authenticate(username=loginusername, password=loginpassword)

        if user:
            if user.is_active:
                login(request, user)
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
        date_posted = datetime.date.today()
        job_place = request.POST.get('place')
        job_description = request.POST.get('job_description')

        if request.user.is_authenticated:
            user = request.user
            check_role = role.objects.get(user=user)
            if check_role.isEmployee:
                myEmployee = employeeProfile.objects.get(user=user)
                post = jobPost(job_title=job_title, experience_required=experience_required, skillset_required=skillset_required,
                            date_posted=date_posted, job_place=job_place, job_description=job_description, employee=myEmployee)
                post.save()
            else:
                HttpResponse('You have no access to this')

        return redirect('index')
    else:
        return render(request, 'jobpost.html')


def joblist(request):
    if request.user.is_authenticated:
        user = request.user
        unmatched = []
        matched = []
        post_data = jobPost.objects.all()
        apply_data = jobApply.objects.all()
        for apply in apply_data:
            if apply.jobseeker.user == user:
                for post in post_data:
                    if apply.jobpost_applied.employee.company == post.employee.company and apply.time_delta != datetime.date.today():
                        pass
                    else:
                        unmatched.append(post.id)

                i = 0
                while(i < len(unmatched)):
                    for post in post_data:
                        if unmatched[i] == post.id:
                                matched.append([post.id, post.job_title, post.employee.company, post.job_place, post.experience_required, post.skillset_required, post.date_posted])
                    i += 1
        if matched:
            context = {'matched': matched}
        else:
            context = {'data': post_data}

        return render(request, 'joblisting.html', context)

def viewinfo(request):
    if request.method == 'GET':
        code = request.GET.get('hiddenName')

        data = jobPost.objects.filter(id=code)
        context = {'data': data}

        return render(request, 'view.html', context)
    else:
        return HttpResponse('404')

def jobapply(request):
    if request.method == 'POST':
        code = request.POST.get('hiddenID')
        if request.user.is_authenticated:
            user = request.user
            check_role = role.objects.get(user=user)
            if check_role.isSeeker:
                seeker = jobseekerProfile.objects.get(user=user)
                post = jobPost.objects.get(id=code)
                date_applied = datetime.date.today()
                time_delta = date_applied + datetime.timedelta(days=1)
                apply = jobApply(jobpost_applied=post, jobseeker=seeker, date_applied=date_applied, time_delta=time_delta)
                apply.save()
            else:
                return HttpResponse('You cannot apply')

        return redirect('index')
    else:
        return HttpResponse('404')
    
def viewapply(request):
    data = jobApply.objects.all()
    context = {'data': data}
    return render(request, 'viewapply.html', context)

def send_mail(request):
    if request.method == 'POST':

        code = request.POST.get('hiddenName')

        data = jobApply.objects.get(id=code)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('referral.solns@gmail.com', 'hr.referral.solns')

        subject = 'The application for the position of ' + data.jobpost_applied.job_title + ' has been received'
        body = 'You submitted the application to ' + data.jobpost_applied.employee.company + ' and your resume was received. Good Luck!'

        msg = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            'referral.solns@gmail.com',
            data.jobseeker.user.email,
            msg
        )
        return redirect('index')