from re import sub
from ResultApp.logic import countTest, deassigStudent, getMutipleUser, studentAvgGrade, testAvgGrade, userTypeFun
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Avg

from ResultApp.models import Classes, Users, UserType, Subjects, StudentClass, StudentSubject, Messages, Result, Tests
from ResultApp.serializers import ClassSerializer, UsersSerializer, UserTypeSerializer, SubjectSerializer, StudentClassSerializer, StudentSubjectSerializer, MessageSerializer, ResultSerializer, TestSerializer


def checkTest(data):
    test = Tests.objects.filter(subject=data['id'])
    count = countTest(test)
    if count == 0:
        return False
    else:
        return True
    
def archiveDeleteSubject(subject):
    subject1 = {}
    if checkTest(subject):
        subject1['id'] = subject['id']
        subject1['name'] = subject['name']
        subject1['description'] = subject['description']
        subject1['classval'] = subject['classval']
        subject1['teacher'] = subject['teacher']
        subject1['archived'] = 'true'
        subject_serializer = SubjectSerializer(subject, data=subject1)
        if subject_serializer.is_valid():
            subject_serializer.save()
        else:
            subject_delete = Subjects.objects.get(id = subject['id'])
            subject_delete.delete()

def teacherArchiveSubject(data):
    subjects = Subjects.objects.filter(teacher=data['id'])
    count = 0
    for subject in subjects:
        if subject['archived'] == False:
            count+=1
    if count == 0:
        return False
    else:
        return True

def removeTeachSubject(subject):
    subject1 = {}
    subject1['id'] = subject['id']
    subject1['name'] = subject['name']
    subject1['description'] = subject['description']
    subject1['classval'] = subject['classval']
    subject1['teacher'] = ''
    subject1['archived'] = subject['archived']
    subject_serializer = SubjectSerializer(subject, data = subject1)
    if subject_serializer.is_valid():
        subject_serializer.save()
     

def subjectTest(results):
    data = []
    tests = Tests.objects.all()
    test_serializer = Tests(tests, many = True)
    for result in results:
        for test in test_serializer.data:
            if result['test'] == test['id']:
                result['subject'] = test['subject']
                data.append(result)
    return data

def subjectAvgMark(subjects, marks):
    data = []
    for subject in subjects:
        count = 0
        sum = 0
        for mark in marks:
            if mark['subject'] == subject['id']:
                count +=1
                sum += mark['marks']
        if count != 0:
            avg = sum/count
            subject['Avgmarks'] = avg
            data.append(subject)
    return data

def studentEnroll(subjects, students):
    data = []
    for subject in subjects:
        val = False
        for student in students:
            if subject['id'] == student['subject']:
                val = True
                break
        subject['enrolled'] = val
        data.append(subject)
    return data
        

def studentTestMap(tests, students):
    data = []
    for test in tests:
        for student in students:
            if student['test'] == test['id']:
                test['marks'] = student['marks']
                data.append(test)
    return data

# Create your views here.

@csrf_exempt
def classApi(request,cid=0):
    if request.method=='GET':
        classes = Classes.objects.all()
        classes_serializer = ClassSerializer(classes, many=True)
        return JsonResponse(classes_serializer.data, safe = False)
    elif request.method =='POST':
        classes_data = JSONParser().parse(request)
        classes_serializer = ClassSerializer(data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Class Added Successfully", safe=False)
        return JsonResponse("Failed To Add class", safe=False)
    elif request.method == 'PUT':
        classes_data = JSONParser().parse(request)
        classes = Classes.objects.get(id = classes_data['id'])
        classes_serializer = ClassSerializer(classes, data = classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Class Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        classes = Classes.object.get(id=cid)
        stuClass = StudentClass.objects.filter(id=cid)
        stuClass_serializer = StudentClassSerializer(stuClass, many=True)
        stuClasses_serializer = StudentClassSerializer(stuClass_serializer.data, data=deassigStudent(stuClass_serializer.data), many=True)
        if stuClass_serializer.is_valid():
            stuClasses_serializer.save()
            subjects = Subjects.objects.filter(classval = cid)
            subjects_serializer = SubjectSerializer(subjects, many = True)
            for subject in subjects_serializer.data:
                archiveDeleteSubject(subject)
            classes.delete()
            return JsonResponse('Classes Deleted Successfully', safe=False)

@csrf_exempt
def UserTypeApi(request):
    if request.method=='GET':
        userType = UserType.objects.all()
        usertype_serializer = UserTypeSerializer(userType, many=True)
        return JsonResponse(usertype_serializer.data, safe = False)
  
@csrf_exempt
def UserLogin(request):
    if request.method=='POST':
        user_data = JSONParser().parse(request)
        user = UserType.objects.filter(username=user_data['username'])
        user_serializer = UserTypeSerializer(user, many=True)
        if user_serializer.data['password'] == user_data['password']:
            return JsonResponse(user_serializer.data, safe = False)
 
@csrf_exempt
def UsersApi(request,uid=0):
    if request.method=='GET':
        users = Users.objects.all()
        stuClass = StudentClass.objects.all()
        users_serializer = UsersSerializer(users, many=True)
        stuClass_serializer = StudentClassSerializer(stuClass, many=True)
        data = getMutipleUser(users_serializer.data, stuClass_serializer.data)
        return JsonResponse(data, safe = False)
    elif request.method =='POST':
        users_data = JSONParser().parse(request)
        user, student = userTypeFun(users_data)
        users_serializer = UsersSerializer(data=user)
        if users_serializer.is_valid():
            users_serializer.save()
            if users_data['usertype'] == 3:
                users_data = Users.objects.get(username=user['username'])
                users_serializer = UsersSerializer(users_data)
                studentclass_serializer = StudentClassSerializer(data={'classval': student['classval'],'students' : users_serializer.data['id']})
                if studentclass_serializer.is_valid():
                    studentclass_serializer.save()
            return JsonResponse("User Added Successfully", safe=False)
        return JsonResponse("Failed To Add user", safe=False)
    elif request.method == 'PUT':
        users_data = JSONParser().parse(request)
        users = Users.objects.get(username = users_data['username'])
        user,stuClass = userTypeFun(users_data)
        users_serializer = UsersSerializer(users, data = users)
        if users_serializer.data['usertype'] == 3:
            users_serializer.save()
            if users_serializer.data['usertype'] == 3:
                stuClasses = StudentClass.objects.get(student = users_serializer.data['id'])
                stuClass_serializer = StudentClassSerializer(stuClasses, data = stuClass)
                if stuClass_serializer.is_valid():
                    stuClass_serializer.save()
            return JsonResponse("Users Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        user = Users.object.get(id=uid)
        user_serializer = UsersSerializer(user)
        if user_serializer.data['usertype'] == 3:
            stuClass = StudentClass.objects.get(students=user_serializer.data['id'])
            stuClass.delete()
            stuSubject = StudentSubject.objects.filter(student=user_serializer.data['id'])
            stuSubject.delete()
            stuResut = Result.objects.filter(student=user_serializer.data['id'])
            stuResut.delete()
            user.delete()
            return JsonResponse('Classes Deleted Successfully', safe=False)
        elif user_serializer.data['usertype'] == 2:
            if teacherArchiveSubject(user_serializer.data) == False:
                teaSubjects = Subjects.objects.filter(teacher=user_serializer.data['id'])
                for teaSubject in teaSubjects:
                    teacherArchiveSubject(teaSubject)
                    user.delete()
            return JsonResponse('Classes Deleted Successfully', safe=False)
        return JsonResponse('Cannot Delete',safe=False)

@csrf_exempt
def SubjectApi(request,sid=0):
    if request.method=='GET':
        subjects = Subjects.objects.all()
        subject_serializer = SubjectSerializer(subjects, many=True)
        return JsonResponse(subject_serializer.data, safe = False)
    elif request.method =='POST':
        subjects_data = JSONParser().parse(request)
        subject_serializer = SubjectSerializer(data=subjects_data)
        print(subject_serializer)
        if subject_serializer.is_valid():
            subject_serializer.save()
            return JsonResponse("Subject Added Successfully", safe=False)
        return JsonResponse("Failed To Add Subject", safe=False)
    elif request.method == 'PUT':
        subject_data = JSONParser().parse(request)
        subjects = Subjects.objects.get(id = subject_data['id'])
        subject_serializer = SubjectSerializer(subjects, data = subject_data)
        if subject_serializer.is_valid():
            subject_serializer.save()
            return JsonResponse("Subject Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        subject = Subjects.object.get(id=sid)
        subject.delete()
        return JsonResponse('Subject Deleted Successfully', safe=False)


@csrf_exempt
def TeacherSubjectApi(request, tid):
    if request.method=='GET':
        subjects = Subjects.objects.all().filter(teacher = tid)
        subject_serializer = SubjectSerializer(subjects, many=True)
        return JsonResponse(subject_serializer.data, safe = False)

@csrf_exempt
def StudentSubjectApi(request, stid):
    if request.method=='GET':
        result = Result.objects.filter(student=stid)
        result_serializer = ResultSerializer(result, many=True)
        mapTestResult = subjectTest(result_serializer.data)
        subjects = Subjects.objects.all()
        subject_serializer = SubjectSerializer(subjects, many=True)
        data = subjectAvgMark(subject_serializer.data, mapTestResult)
        return JsonResponse(data, safe = False)

@csrf_exempt
def EnrollSubject(request, stid):
    if request.method=='GET':
        stuclass = StudentClass.objects.filter(students = stid)
        stuclass_serializer = StudentClassSerializer(stuclass)
        stuSubject = Subjects.objects.filter(student = stid)
        stuSubject_serializer = SubjectSerializer(stuSubject, many = True)
        subjects = Subjects.objects.filter(classval = stuclass_serializer.data['classval'])
        subjects_serializer = SubjectSerializer(subjects, many = True)
        data = studentEnroll(subjects_serializer.data, stuSubject_serializer.data)
        return JsonResponse(data, safe = False)
    elif request.method=='POST':
        stuSubject_data = JSONParser().parse(request)
        stuSubject_serializer = StudentSubjectSerializer(stuSubject_data)
        if stuSubject_serializer.is_valid():
            stuSubject_serializer.save()
            return JsonResponse('Enrolled Successfuly', safe = False)
        return JsonResponse('Cannot Enrolled', safe = False)
    elif request.method == 'Delete':
        stuSubject_data = JSONParser().parse(request)
        stuSubject_serializer = StudentSubjectSerializer(stuSubject_data)
        stuSubject = StudentSubject.objects.filter(subject = stuSubject_serializer.data['subject'],student = stid)
        stuSubject.delete()
        return JsonResponse('UnEnrolled successfull', safe = False)
 


@csrf_exempt
def TeacherTestApi(request, sid, tid=0):
    if request.method=='GET':
        test = Tests.objects.all().filter(subject =sid )
        result = Result.objects.values('test').annotate(avgGrade = Avg('marks'))
        test_serializer = TestSerializer(test, many = True)
        data = testAvgGrade(test_serializer.data, result)
        return JsonResponse(data, safe=True)
    elif request.method=='POST':
        test = JSONParser().parse(request)
        test_serializer = TestSerializer(data=test)
        if test_serializer.is_valid():
            test_serializer.save()
            return JsonResponse('Test Added Successfully', safe = False)
        return JsonResponse('Failde To Add Test', safe = False)
    elif request.method == 'PUT':
        test_data = JSONParser().parse(request)
        test = Tests.objects.get(id = test_data['id'])
        test_serializer = TestSerializer(test, data= test_data)
        if test_serializer.is_valid():
            test_serializer.save()
            return JsonResponse('Test Update Successfully', safe=False)
        return JsonResponse('Failed To update Test', safe=False)
    elif request.method == 'DELETE':
        test = Tests.objects.get(id = tid)
        test_serializer = TestSerializer(test, many = True)
        result = Result.objects.filter(test = test_serializer.data['id'])
        result.delete()
        test.delete()
        return JsonResponse('Test Deleted successfully')

@csrf_exempt
def TeacherStudentTestApi(request, sid):
    if request.method=='GET':
        test = Tests.objects.all().filter(subject =sid)
        result = Result.objects.values('test','student').annotate(avgGrade = Avg('marks'))
        student = Users.objects.all().filter(usertype = 3)
        test_serializer = TestSerializer(test, many = True)
        student_serializer = UsersSerializer(student, many=True)
        data = studentAvgGrade(test_serializer.data,student_serializer.data, result)
        return JsonResponse(data, safe=True)

@csrf_exempt
def StudentTestApi(request, sid,stid):
    if request.method=='GET':
        test = Tests.objects.all().filter(subject=sid)
        test_serializer = TestSerializer(test, many = True)
        result = Result.objects.filter(student=stid)
        result_serializer = ResultSerializer(result, many = True)
        data = studentTestMap(test_serializer.data, result_serializer.data)
        return JsonResponse(data, safe=True)

@csrf_exempt
def TeacherResultApi(request, tid, rid = 0):
    if request.method == 'GET':
        result = Result.objects.all().filter(test =tid)
        result_serializer = ResultSerializer(result, many=True)
        return JsonResponse(result_serializer.data, safe=True)
    elif request.method == 'POST':
        result = JSONParser().parse(request)
        result_serializer = ResultSerializer(data=result)
        if result_serializer.is_valid():
            result_serializer.save()
            return JsonResponse('Result Added Successfully', safe=True)
        JsonResponse('Failed To Add Result', safe=False)
    elif request.method == 'PUT':
        result_data = JSONParser().parse(request)
        result = Result.objects.get(id = result_data['id'])
        result_serializer = ResultSerializer(result, data = result_data)
        if result_serializer.is_valid():
            result_serializer.save()
            return JsonResponse('Updated the result', safe=False)
        return JsonResponse('Failed To update result', safe=False)
    elif request.method == 'DELETE':
        result = Result.objects.get(id = rid)
        result.delete()
        return JsonResponse('Result delete successfully', safe=False)


@csrf_exempt
def StudentResultApi(request,sid,tid):
    if request.method == 'GET':
        result = Result.objects.all().filter(test = tid).filter(student=sid)
        result_serializer = ResultSerializer(result, many=True)
        return JsonResponse(result_serializer.data, safe=True)
        

@csrf_exempt
def MessageAPI(request, uid):
    if request.method == 'GET':
        user_data = Users.objects.filter(id = uid)
        user_serializer = UsersSerializer(user_data)
        messages = Messages.objects.all().filter(sender=user_serializer.data['username']).filter(reviver = user_serializer.data['username'])
        messages_serializer = MessageSerializer(messages, many=True)
        return JsonResponse(messages_serializer, safe=False)
    elif request.method=='POST':
        messages = JSONParser().parse(request)
        messages_serializer = MessageSerializer(data=messages)
        if messages_serializer.is_valid():
            messages_serializer.save()
            return JsonResponse('messages is added', safe=False)
        return JsonResponse('Message could be added', safe=False)

