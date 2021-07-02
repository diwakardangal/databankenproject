from django.conf.urls import url
from ResultApp import views

urlpatterns = [
    url(r'^classes/$', views.classApi),
    url(r'^classes/([0-9]+)$', views.classApi),
    url(r'^users/$', views.UsersApi),
    url(r'^subjects/$', views.SubjectApi),
    url(r'^subjects/([0-9]+)/$', views.SubjectApi),
    url(r'^teacher/([0-9]+)/subjects/$', views.TeacherSubjectApi),
    url(r'^student/([0-9]+)/subjects/$', views.StudentSubjectApi),
    url(r'^student/([0-9]+)/allsubject/', views.EnrollSubject),
    url(r'^teacher/subjects/([0-9]+)/test/$', views.TeacherTestApi),
    url(r'^teacher/subject/([0-9]+)/test/([0-9]+)/$',views.TeacherTestApi),
    url(r'^teacher/subject/[0-9]+)/student/([0-9]+)/$', views.TeacherStudentTestApi),
    url(r'teacher/subject/[0-9]+)/result/$', views.TeacherResultApi),
    url(r'teacher/subject/[0-9]+)/result/([0-9]+)/$', views.TeacherResultApi),
    url(r'student/([0-9]+)/result/([0-9]+)/$', views.StudentResultApi),
    url(r'user/([0-9]+)/messages/$', views.MessageAPI)
]
