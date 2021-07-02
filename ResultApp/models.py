from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

# Create your models here.

class Classes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

class UserType(models.Model):
    id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=10,unique=True)

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50,unique=True)
    forname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    usertype = models.ForeignKey(UserType,on_delete=models.CASCADE)
    
class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    classval = models.ForeignKey(Classes,null=True,on_delete=models.SET_NULL)
    teacher = models.ForeignKey(Users,null=True,on_delete=models.SET_NULL)
    archived = models.BooleanField(default= False)

class StudentClass(models.Model):
    id = models.AutoField(primary_key=True)
    classval = models.ForeignKey(Classes,null=True,on_delete=SET_NULL)
    students = models.ForeignKey(Users,on_delete=models.CASCADE)

class StudentSubject(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subjects,null=True,on_delete=SET_NULL)
    student = models.ForeignKey(Users,on_delete=models.CASCADE)
    
class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=50) 
    reviever = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    status = models.BooleanField(default=True)

class Tests(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    dateOfTest = models.DateField()

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Users,on_delete=models.CASCADE)
    test = models.ForeignKey(Tests,on_delete=models.CASCADE)
    marks = models.FloatField()

