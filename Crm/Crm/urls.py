"""Crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path,include
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/',views.reg),

    path('register/', views.RegisterView.as_view()),

    path('login/',views.login),
    path('index/',views.index),
    path('get_valid_img/',views.get_valid_img),
    path('customers/list/', views.CustomerView.as_view(), name="customers_list"),
    path('customers/self/', views.CustomerView.as_view(),name = "customers_self"),
    path("customers/all/",views.CustomerView.as_view()),
    path('logout/', views.logout),
    path('customers/add/',views.AddCustomerView.as_view(),name="addcustomers"),
    re_path('customer/edit/(\d+)', views.EditCustomerView.as_view(),name="editcustomers"),
    re_path('customer/del/(\d+)', views.EditCustomerView.as_view(),name="delcustomers"),
    path('customer/recoder/self/',views.RecoderCustomerView.as_view(),name='recodercustomer'),
    path('customer/recoder/public/',views.RecoderCustomerView.as_view(),name='recoderpublic'),
    path('customer/recoder/',views.RecoderCustomerView.as_view(),name='recoder'),
    path('recoder/add/',views.AddrecoderCustomer.as_view(),name="addrecoder"),
    re_path('recoder/edit/(\d+)',views.EditrecodrView.as_view(),name="editrecoder"),
    re_path('recoder/del/(\d+)',views.EditrecodrView.as_view(),name="delrecoder"),
    path('Enrollment/list/',views.EnrollmentView.as_view(),name='enroll'),
    re_path('Enrollment/edit/(\d+)',views.EditAddenrollment.as_view(),name='enrolledit'),
    re_path('Enrollment/add/',views.EditAddenrollment.as_view(),name='enrolladd'),

    # 班级学习记录  #批量创建走的这个路径
    path("ClassStudyRecord/list/",views.ClassStudyRecordView.as_view(),name = "classsturecoder"),
    re_path("ClassStudyRecord/edit/(\d+)",views.ClassStudyRecordAdd_Edit.as_view(),name = "classstuedit"),
    path("ClassStudyRecord/add/",views.ClassStudyRecordAdd_Edit.as_view(),name = "classstuadd"),
    re_path("ClassStudyRecord/del/(\d+)",views.ClassStudyRecordAdd_Edit.as_view(),name = "classstudel"),

    # 学生学习记录
    path("StudentStudyRecord/list/", views.StudentStudyRecordView.as_view(), name="studentsturecoder"),
    re_path("StudentStudyRecord/edit/(\d+)", views.StudentStudyRecordAdd_Edit.as_view(), name="studentstuedit"),
    path("StudentStudyRecord/add/", views.StudentStudyRecordAdd_Edit.as_view(), name="studenttuadd"),
    re_path("StudentStudyRecord/del/(\d+)", views.StudentStudyRecordAdd_Edit.as_view(), name="studentstudel"),

    # 录入分数
    re_path('ScoreRecord/show/(\d+)/', views.RecordScoreView.as_view(), name="record_score"),
    path('customer/tongji/', views.TongJiView.as_view(), name="tongji"),
    re_path(r'', include('rbac.urls', )),
]
