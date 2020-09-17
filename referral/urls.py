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
]