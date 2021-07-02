from itertools import product

def userTypeFun(data):
    user = {}
    student = {}
    user['username'] = data['username']
    user['forname'] = data['forname']
    user['lastname'] = data['lastname']
    user['password'] = data['password']
    user['usertype'] = data['usertype']
    if data['usertype'] == 3:
        student['classval'] = data['classval']
    return user,student

def returnClassStudent(user,stuClass):
    data = {}
    data['username'] = user['username'] 
    data['forname'] = user['forname'] 
    data['lastname'] = user['lastname']
    data['password'] = user['password']
    data['usertype']= user['usertype']
    if user['usertype'] == 3:
        data['classval'] = stuClass['classval']
    else:
        data['classval'] = ''
    return data

def getMutipleUser(users,stuClass):
    data = []
    for user in users:
        if user['usertype'] == 3:
            for stu in stuClass:
                if user['id'] == stu['students']:
                    user['classval'] = stu['classval']
                    break
        else:
            user['classval'] = ''
        data.append(user)
    return data

def deassigStudent(stuClasses):
    for stuClass in stuClasses:
        stuClass['classval'] = 0
    return stuClasses

def countTest(tests):
    count = 0
    for test in tests:
        count+=1
    return count

def testAvgGrade(tests, grades):
    data =[]
    for test in tests:
        test['avgGrade'] = 0
        for grade in grades:
            if test['id'] == grade['test']:
                test['avgGrade'] = grade['avgGrade']
                data.append(test)
                continue
    return data

def studentAvgGrade(tests,students,grades):
    data = []
    for test, student in product(tests, students):
        student['avgGrade'] = 0
        for grade in grades:
            if test['id'] == grade['test'] and student['id'] == grade['student'] and test['student'] == student['id']:
                test['avgGrade'] = grade['avgGrade']
                data.append(test)
    return data
                

