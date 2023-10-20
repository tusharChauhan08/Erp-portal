from django.shortcuts import render,redirect
import pymongo
import re
import base64
from pymongo.errors import ConnectionFailure

class Prishni:
    def __init__(self):
        self.passSetError = False
        self.idError = False
        self.signupError = False
        self.logoutOpt = False
        self.result = [0]
        self.adminId = ''
        self.teachId = ''
        self.studentId = ''
        try:
            self.connection = pymongo.MongoClient('mongodb://127.0.0.1:27017')
            self.database = self.connection['Prishni']
            self.collection1 = self.database['Admin']
            self.collection2 = self.database['TeacherDetail']
            self.collection3 = self.database['StudentDetail']
            self.collection4 = self.database['CertificateDetail']
        except ConnectionFailure:
            print('Could not connect to the server')

    # Logout of the admin
    def adminLogout(self, request):
        request.session.flush()
        return redirect('/adminLogin?=logoutSuccessfully')

    # Home Page
    def adminHome(self, request):
        if request.session.has_key('user'):
            self.logoutOpt = True
            self.query = {
                'Admin_id': self.adminId,
            }
            self.teacherResult = []
            for self.x in self.collection2.find(self.query):
                self.teacherResult.append(self.x)
            return render(request,'admin/adminHome.html',{'logoutOpt': self.logoutOpt,'teacherResult': self.teacherResult})
        else:
            self.logoutOpt = False
            return redirect('/adminLogin?=notAuthorized')

    # Admin Signup
    def adminSignup(self, request):
        for self.x in self.collection1.find({}):
            self.result[0] = self.x
        if self.result[0] == 0:
            return render(request, 'admin/adminSignup.html',{'passSetError': self.passSetError, 'signupError': self.signupError, 'idError': self.idError})
        else:
            return redirect('/adminLogin?=AdminIsAlreadyRegister')

    def adminPost(self, request):
        try:
            if request.method == "POST":
                self.reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
                self.matchRe = re.compile(self.reg)
                self.name = request.POST.get('name')
                self.mobile = request.POST.get('mobile')
                self.email = request.POST.get('email')
                self.password = request.POST.get('password')
                self.resultPass = re.search(self.matchRe, self.password)
                self.passwordEncoded = base64.b64encode(self.password.encode('utf-8'))
                self.data = ({
                    'Name': self.name,
                    'Mobile_no': self.mobile,
                    'Email_id': self.email,
                    'Password': self.passwordEncoded
                })
                self.query = {
                    "Email_id": self.email
                }
                self.result = [0]
                for self.x in self.collection1.find(self.query):
                    self.result[0] = self.x
                if self.resultPass and self.result[0] == 0 and self.name != "" and self.mobile != "" and self.email != "" and self.password != "":
                    self.passSetError = False
                    self.signupError = False
                    self.idError = False
                    self.collection1.insert_many([self.data])
                    self.logoutOpt = True
                    return redirect("/adminSignup?=success")
                elif self.result[0] != 0:
                    self.signupError = False
                    self.passSetError = False
                    self.idError = True
                    return redirect("/adminSignup?=idFoundFail")
                elif self.name == "" or self.mobile == "" or self.email == "" or self.password == "":
                    self.idError = False
                    self.signupError = True
                    return redirect("/adminSignup?=notAllFill")
                else:
                    self.passSetError = True
                    return redirect('/adminSignup?=passValidFailed')
        except:
            print("Data is not Fetched from the database.")
            return redirect("/adminSignup?=serverFail")

    # Admin Login
    def adminLogin(self, request):
        return render(request, 'admin/adminLogin.html',{'passSetError': self.passSetError, 'signupError': self.signupError, 'idError': self.idError})

    def adminLoginPost(self, request):
        try:
            if request.method == "POST":
                self.email = request.POST.get('email')
                self.password = request.POST.get('password')
                self.query = {
                    "Email_id": self.email,
                }
                self.result = [0]
                for self.x in self.collection1.find(self.query):
                     self.result[0] = self.x
                if self.email != '' and self.password != "" and self.result[0] != 0:
                    self.signupError = False
                    self.idError = False
                    self.passwordDecoded = base64.b64decode(self.result[0]['Password']).decode('utf-8')
                    if self.passwordDecoded == self.password:
                        self.passSetError = False
                        self.logoutOpt = True
                        request.session['user'] = self.email
                        self.adminId = self.result[0]['_id']
                        return redirect('/adminHome?=success')
                    else:
                        self.passSetError = True
                        return redirect('/adminLogin?=passwordFailed')
                elif self.email == '' or self.password == "":
                    self.idError = False
                    self.signupError = True
                    return redirect('/adminLogin?=idNotFound')
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect('/adminLogin?=entryNotFull')
        except:
            print("Data is not fetched from the database.")
            return redirect('/adminLogin?=serverFail')

    def createTeacher(self, request):
        if request.session.has_key('user'):
            return render(request, 'admin/createTeacher.html',{'signupError': self.signupError, 'idError': self.idError})
        else:
            return redirect('/adminLogin?=notAuthorized')

    def createPost(self, request):
        try:
            if request.method == "POST":
                self.name = request.POST.get('name')
                self.mobile = request.POST.get('mobile')
                self.email = request.POST.get('email')
                self.teacherId = request.POST.get('teacherId')
                self.course = request.POST.get('course')
                self.data = ({
                    'Name': self.name,
                    'Mobile_no': self.mobile,
                    'Email_id': self.email,
                    'Teacher_id': self.teacherId,
                    'Admin_id': self.adminId,
                    'Course': self.course
                })
                self.query = {
                    "Email_id": self.email
                }
                self.result = [0]
                for self.x in self.collection2.find(self.query):
                    self.result[0] = self.x
                if self.result[0] == 0 and self.name != "" and self.mobile != "" and self.email != ""  and self.teacherId != "" and self.course != "":
                    self.signupError = False
                    self.idError = False
                    self.collection2.insert_many([self.data])
                    return redirect("/createTeacher?=success")
                elif self.name == "" or self.mobile == "" or self.email == ""  or self.teacherId == "" or self.course == "":
                    self.idError = False
                    self.signupError = True
                    return redirect("/createTeacher?=notAllFill")
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect("/createTeacher?=idFoundFail")
        except:
            print("Data is not Fetched from the database.")
            return redirect("/adminHome?=serverFail")

    # Teacher Logout
    def teacherLogout(self, request):
        request.session.flush()
        return redirect('/?=logoutSuccessfully')
    # Teacher Dashboard
    def teacherHome(self, request):
        if request.session.has_key('teacherUser') or request.session.has_key('user'):
            self.logoutOpt = True
            self.studentResult = []
            self.studentQuery = {
                "Teacher_id": self.teachId,
            }
            for self.x in self.collection3.find(self.studentQuery):
                self.studentResult.append(self.x)
            return render(request, 'teacher/teacherHome.html', {'logoutOpt': self.logoutOpt, 'studentResult': self.studentResult})
        else:
            self.logoutOpt = False
            return redirect('/?=notAuthorized')


    # Teacher Login
    def teacherLogin(self, request):
        return render(request, 'teacher/teacherLogin.html',{'signupError': self.signupError, 'idError': self.idError, 'passSetError': self.passSetError})

    def teacherLoginPost(self, request):
        try:
            if request.method == "POST":
                self.email = request.POST.get('email')
                self.teacherId = request.POST.get('teacherId')
                self.query = {
                    "Email_id": self.email,
                }
                self.result = [0]
                for self.x in self.collection2.find(self.query):
                     self.result[0] = self.x
                if self.email != '' and self.teacherId != "" and self.result[0] != 0:
                    self.signupError = False
                    self.idError = False
                    if self.result[0]["Teacher_id"] == self.teacherId:
                        self.passSetError = False
                        self.logoutOpt = True
                        request.session['teacherUser'] = self.email
                        self.teachId = self.result[0]['_id']
                        return redirect('/teacherHome?=success')
                    else:
                        self.passSetError = True
                        return redirect('/?=passwordFailed')
                elif self.email == '' or self.teacherId == "":
                    self.idError = False
                    self.signupError = True
                    return redirect('/?=idNotFound')
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect('/?=entryNotFull')
        except:
            print("Data is not fetched from the database.")
            return redirect('/?=serverFail')

    # Create Student
    def createStudent(self, request):
        if request.session.has_key('teacherUser'):
            return render(request, 'teacher/createStudent.html', {'signupError': self.signupError, 'idError': self.idError})
        else:
            return redirect('/teacherHome?=notAuthorized')

    def studentPost(self, request):
        try:
            if request.method == "POST":
                self.name = request.POST.get('name')
                self.mobile = request.POST.get('mobile')
                self.email = request.POST.get('email')
                self.dob = request.POST.get('dob')
                self.course = request.POST.get('course')
                self.data = ({
                    'Name': self.name,
                    'Mobile_no': self.mobile,
                    'Email_id': self.email,
                    'Student_DOB': self.dob,
                    'Teacher_id': self.teachId,
                    'Course': self.course
                })
                self.query = {
                    "Email_id": self.email
                }
                self.result = [0]
                for self.x in self.collection3.find(self.query):
                    self.result[0] = self.x
                if self.result[0] == 0 and self.name != "" and self.mobile != "" and self.email != "" and self.dob != "" and self.course != "":
                    self.signupError = False
                    self.idError = False
                    self.collection3.insert_many([self.data])
                    return redirect("/teacherHome/createStudent?=success")
                elif self.name == "" or self.mobile == "" or self.email == "" or self.dob == "" or self.course == "":
                    self.idError = False
                    self.signupError = True
                    return redirect("/teacherHome/createStudent?=notAllFill")
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect("/teacherHome/createStudent?=idFoundFail")
        except:
            print("Data is not Fetched from the database.")
            return redirect("/teacherHome?=serverFail")



    # Create Certificate
    def createCertificate(self, request):
        if request.session.has_key('teacherUser'):
            return render(request, 'teacher/certificateInfo.html', {'signupError': self.signupError, 'idError': self.idError})
        else:
            return redirect('/teacherLogin?=notAuthorized')

    def createCertificatePost(self, request):
        try:
            if request.method == "POST":
                self.name = request.POST.get('name')
                self.course = request.POST.get('course')
                self.startDate = request.POST.get('startDate')
                self.endDate = request.POST.get('endDate')
                self.marks = request.POST.get('marks')
                self.email = request.POST.get('email')
                self.studentQuery = {
                    'Email_id': self.email,
                    'Teacher_id': self.teachId,
                }
                self.data = ({
                    'Name': self.name,
                    'Start_Date': self.startDate,
                    'End_Date': self.endDate,
                    'Teacher_id': self.teachId,
                    'Course': self.course,
                    'Marks': self.marks,
                    'Email_id': self.email,
                })
                self.result = [0]
                for self.x in self.collection3.find(self.studentQuery):
                    self.result[0] = self.x
                if self.result[0] != 0 and self.name != "" and self.startDate != "" and self.endDate != "" and self.course != "" and self.marks != "" and self.email != "":
                    self.signupError = False
                    self.idError = False
                    self.collection4.insert_many([self.data])
                    return redirect("/teacherHome/createCertificate?=success")
                elif self.name == "" or self.startDate == "" or self.endDate == "" or self.course == "" or self.marks == "" or self.email == "":
                    self.idError = False
                    self.signupError = True
                    return redirect("/teacherHome/createCertificate?=notAllFill")
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect("/teacherHome/createCertificate?=idFoundFail")
        except:
            print("Data is not Fetched from the database.")
            return redirect("/teacherHome?=serverFail")


    # This is for the teacher to show the student certificate by his dashboard
    def showCertificate(self, request):
        if request.session.has_key('teacherUser'):
            return render(request, 'teacher/showCertificate.html',{'signupError': self.signupError, 'idError': self.idError})
        else:
            return redirect('/teacherHome?=notAuthorized')

    def showCertificatePost(self, request):
        try:
            if request.method == "POST":
                self.email = request.POST.get('email')
                self.query = {
                    "Email_id": self.email,
                    "Teacher_id": self.teachId
                }
                self.result = [0]
                for self.x in self.collection4.find(self.query):
                    self.result[0] = self.x
                if self.email != '' and self.result[0] != 0:
                    self.signupError = False
                    self.idError = False
                    request.session['studentEmail'] = self.email
                    return redirect('/teacherShowCertificate?=success')
                elif self.email == '':
                    self.idError = False
                    self.signupError = True
                    return redirect('/showCertificate?=idNotFound')
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect('/showCertificate?=entryNotFull')
        except:
            print("Data is not fetched from the database.")
            return redirect('/teacherHome?=serverFail')

    # Teacher Show url for student certificate
    def teacherShowCertificate(self, request):
        if request.session.has_key('teacherUser'):
            self.studentQuery = {
                "Email_id": request.session['studentEmail'],
            }
            self.studentResult = [0]
            for self.x in self.collection4.find(self.studentQuery):
                self.studentResult[0] = self.x
            return render(request, 'student/studentCertificate.html', {'studentResult': self.studentResult})
        else:
            return redirect('/studentLogin?=notAuthorized')



    # student logout
    def studentLogout(self, request):
        request.session.flush()
        return redirect('/studentLogin?=logoutSuccessfully')

    # Student View
    def studentHome(self, request):
        if request.session.has_key('studentUser'):
            self.logoutOpt = True
            self.teacherQuery = {
                "_id": self.studentId,
            }
            self.teacherResult = []
            for self.x in self.collection2.find(self.teacherQuery):
                self.teacherResult.append(self.x)
            return render(request, 'student/studentHome.html',{'logoutOpt': self.logoutOpt, 'teacherResult': self.teacherResult})
        else:
            self.logoutOpt = False
            return redirect('/studentLogin?=notAuthorized')

    # student Login
    def studentLogin(self, request):
        return render(request, 'student/studentLogin.html',{'signupError': self.signupError, 'idError': self.idError})
    def studentLoginPost(self, request):
        try:
            if request.method == "POST":
                self.email = request.POST.get('email')
                self.dob = request.POST.get('dob')
                self.query = {
                    "Email_id": self.email,
                }
                self.result = [0]
                for self.x in self.collection3.find(self.query):
                    self.result[0] = self.x
                if self.email != '' and self.dob != "" and self.result[0] != 0:
                    self.signupError = False
                    self.idError = False
                    if self.result[0]["Student_DOB"] == self.dob:
                        self.passSetError = False
                        self.logoutOpt = True
                        request.session['studentUser'] = self.email
                        self.studentId = self.result[0]['Teacher_id']
                        return redirect('/studentHome?=success')
                    else:
                        self.passSetError = True
                        return redirect('/studentLogin?=passwordFailed')
                elif self.email == '' or self.dob == "":
                    self.idError = False
                    self.signupError = True
                    return redirect('/studentLogin?=idNotFound')
                else:
                    self.signupError = False
                    self.idError = True
                    return redirect('/studentLogin?=entryNotFull')
        except:
            print("Data is not fetched from the database.")
            return redirect('/studentHome?=serverFail')


    # Student Certificate show url
    def studentCertificate(self, request):
        print(request.session.has_key('studentUser'))
        if request.session.has_key('studentUser'):
            self.studentQuery = {
                "Email_id": request.session['studentUser'],
            }
            self.studentResult = [0]
            for self.x in self.collection4.find(self.studentQuery):
                self.studentResult[0] = self.x
            return render(request, 'student/studentCertificate.html',{'studentResult': self.studentResult})
        else:
            return redirect('/studentLogin?=notAuthorized')