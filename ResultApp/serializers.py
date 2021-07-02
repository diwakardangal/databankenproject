from django.db import models
from rest_framework import fields, serializers
from ResultApp.models import Classes, UserType, Users, Subjects, StudentClass, StudentSubject, Messages, Tests, Result

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ('id', 
            'name', 
            'description')

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('id',
            'Type')

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id',
            'username',
            'forname',
            'lastname',
            'password',
            'usertype',
            )
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ('id',
            'name',
            'description',
            'classval',
            'teacher',
            'archived')

class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ('id',
            'classval',
            'students')

class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = ('id',
            'subject',
            'student')
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        models = Messages
        fields = ('id',
            'sender',
            'reviever',
            'subject',
            'description',
            'date',
            'status')

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = ('id',
            'name',
            'subject',
            'dateOfTest')

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id',
        'student',
        'test',
        'marks')