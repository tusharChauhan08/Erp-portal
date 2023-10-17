"""prishni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from prishni import views

edutechObj = views.Prishni()

urlpatterns = [
    # routes for the admin of the institute
    path('admin/', admin.site.urls),
    path('adminHome', edutechObj.adminHome),
    path('adminSignup', edutechObj.adminSignup),
    path('adminSignup/signupPost', edutechObj.adminPost),
    path('adminLogin', edutechObj.adminLogin),
    path('adminLogin/loginPost', edutechObj.adminLoginPost),
    path('adminLogout', edutechObj.adminLogout),
    path('createTeacher', edutechObj.createTeacher),
    path('adminHome/createPost', edutechObj.createPost),

    # routes for the teacher of the institute
    path('teacherHome', edutechObj.teacherHome),
    path('', edutechObj.teacherLogin),
    path('teacherLogin', edutechObj.teacherLoginPost),
    path('teacherLogout', edutechObj.teacherLogout),
    path('teacherHome/createStudent', edutechObj.createStudent),
    path('teacherHome/studentPost', edutechObj.studentPost),
    path('teacherHome/createCertificate', edutechObj.createCertificate),
    path('teacherHome/certificatePost', edutechObj.createCertificatePost),
    path('showCertificate', edutechObj.showCertificate),
    path('showCertificatePost', edutechObj.showCertificatePost),
    # routes for the student of the institute
    path('studentHome', edutechObj.studentHome),
    path('studentLogin', edutechObj.studentLogin),
    path('studentHome/studentLoginPost', edutechObj.studentLoginPost),
    path('studentLogout', edutechObj.studentLogout),
    path('studentCertificate', edutechObj.studentCertificate),
]

