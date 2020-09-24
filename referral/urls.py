from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),
    path('signup/', views.employeeSignup, name='signup'),
    path('jobapply/', views.jobapply, name='jobapply'),
    path('joblist/', views.joblist, name='joblist'),
    path('jobpost/', views.job_post, name='jobPost'),
    path('seekerSignup/', views.seekerSignup, name='seekerSignup'),
    path('viewinfo/', views.viewinfo, name='viewinfo'),
    path('viewapply/', views.viewapply, name='viewapply'),
    path('sendmail/', views.send_mail, name='sendmail'),
]