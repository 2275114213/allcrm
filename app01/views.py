import json

from django.shortcuts import render, redirect, HttpResponse
# from django.contrib import auth
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from django.conf import settings
from app01.models import *
from app01.page import Pagination
from app01.forms.Userform import UserModelForm

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_tasks.email_tasks import  send_register_active_email
def reg(request):
    respon = {'user': None, 'errors': ''}
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'reg.html', {"form": form})
    else:
        print('hahaasad', request.POST)
        form = UserModelForm(request.POST)
        print('youcuo', type(form))
        if form.is_valid():
            user = form.save()
            username = request.POST.get('username')
            email = request.POST.get('email')
            serializer = Serializer(settings.SECRET_KEY, 3600)
            info = {'confirm': user.id}
            token = serializer.dumps(info)  # bytes
            token = token.decode()
            send_register_active_email.delay(email, username, token)
            respon['user'] = request.POST.get('username')
        else:
            print(form.errors)
            respon['errors'] = form.errors
        return JsonResponse(respon)


class RegisterView(View):
    form_cls = UserModelForm

    def get(self, request):
        form = self.form_cls()
        return render(request, 'reg.html', {"form": form})

    def post(self, request):
        response = {'user': None, 'errors': ''}
        form = self.form_cls(request.POST)
        if form.is_valid():
            user = form.save()  # model 的forms 组件就帮我们进行了create了,不用我们自己create

            response['user'] = request.POST.get('username')
        else:
            response['errors'] = form.errors
        return JsonResponse(response)


from rbac.models import User1


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:

        response = {"user": None, "err_msg": ""}

        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        validcode = request.POST.get("validcode")

        # 如果验证码不相等的情况下, 提示错误信息
        if validcode.upper() != request.session.get("keep_str").upper():
            response["error"] = "验证码错误！"
            return HttpResponse(json.dumps(response))

        # 验证码的校验写进django -session 里
        # 如果明文就用这句,如果是密文就
        # user_obj = auth.authenticate(username=user,password=pwd)
        user_obj = User1.objects.filter(name=user, pwd=pwd).first()

        # 校验用户名和密码
        if not user_obj:
            response['error'] = "用户名或者密码错误！"
            return HttpResponse(json.dumps(response))

        # auth.login(request,user_obj) 登陆
        request.session['user_id'] = user_obj.pk
        response["user"] = user
        from rbac.service.rbac import initial_session
        initial_session(request, user_obj)
        return HttpResponse(json.dumps(response))


def get_valid_img(request):
    #  方式1：读取指定图片
    # with open("static/img/valid.jpg","rb") as f:
    #     data=f.read()

    # 方式2：基于PIL模块创建验证码图片
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO

    def get_random_color():
        import random
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    #
    # img=Image.new("RGB",(350,38),get_random_color())
    # f=open("valid.png","wb")
    # img.save(f,"png")
    # with open("valid.png","rb") as f:
    #     data=f.read()

    # 方式3：
    # img=Image.new("RGB",(350,38),get_random_color())
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()

    # # 方式4:完善文本
    #
    # img=Image.new("RGB",(350,38),get_random_color())
    # draw=ImageDraw.Draw(img)
    # font=ImageFont.truetype("static/font/kumo.ttf",32)
    # draw.text((0,0),"python!",get_random_color(),font=font)
    #
    # # 写与读
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()

    # 方式5:

    img = Image.new("RGB", (350, 38), get_random_color())
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/kumo.ttf", 32)

    keep_str = ""
    for i in range(6):
        import random
        random_num = str(random.randint(0, 9))
        random_lowalf = chr(random.randint(97, 122))
        random_upperalf = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_lowalf, random_upperalf])
        draw.text((i * 30 + 50, 0), random_char, get_random_color(), font=font)
        keep_str += random_char

    # width=350
    # height=38
    # for i in range(100):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_random_color())
    #
    # for i in range(500):
    #     draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    # 写与读
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()

    print('keep_str', keep_str)

    # 将验证码存在各自的session中

    request.session['keep_str'] = keep_str

    return HttpResponse(data)


def index(request):
    return render(request, 'index.html')


def logout(request):
    # 需要参数
    auth.logout(request)
    return redirect('/login/')


# 修改密码
def set_password(request):
    user = User.objects.get(username=request.user.username)
    user.set_password(raw_password="666")
    user.save()
    return redirect("/login/")


# instance = A()
# print getattr(Instance , 'name, 'not find') #如果Instance 对象中有属性name则打印self.name的值，否则打印'not find'
from django.views import View
from app01.models import Campuses
from app01.models import UserInfo
from app01.models import Customer
def get_link_tags(request):
    link_dict = {}
    link_list = ['status','campuses',"consultant"]
    for field in link_list:
        print('field', field)
        import copy
        params = copy.deepcopy(request.GET)
        tmp = []
        if field == 'status':
            a_list = Customer.enroll_status_choices
            title = Customer._meta.get_field(field).verbose_name
        if field == 'campuses':
            a_list = Campuses.objects.all().values_list('pk','name')
            '''
            value : [{'pk': 1, 'name': '北京'}, {'pk': 2, 'name': '上海'}, {'pk': 3, 'name': '深圳'}]>
            value_list : [(1, '北京'), (2, '上海'), (3, '深圳')]
            '''
            title = Campuses._meta.get_field('name').verbose_name
        if field == 'consultant':
            a_list = Customer._meta.get_field(field).remote_field.model.objects.all().values_list('pk','username')
            print('===============', a_list)
            title = Customer._meta.get_field(field).verbose_name

        # if field == 'campuses':
        #     a_list
        #     pass
        # if
        for i, j in a_list:

            params[field] = i
            _url = params.urlencode()
            text = j
            tmp.append('<a href="?%s">%s</a>'%(_url,text))
        link_dict[title] = tmp
        print('link_dict',link_dict)
    return  link_dict

class CustomerView(View):

    # params = copy.deepcopy(request.GET)
    # 展示我的客户,所有客户
    dic = {}



    def get(self, request):
        print(request.GET)
        get_link_tags(request)
        for field, val in request.GET.items():
            try:
                if not val:
                    self.dic.pop(field)
            except KeyError:
                continue
            else:
                self.dic[field] = val

        ret = self.dic
        print("divc", self.dic)
        links = get_link_tags(request)



        if request.path == reverse('customers_list'):
            lable = '公户列表'
            # 没有销售的是公户列表
            customers_list = Customer.objects.filter(consultant__isnull=True, )
            print(customers_list)
        elif request.path == "/customers/all/":
            lable = '所有报名客户列表'
            customers_list = Customer.objects.filter(**self.dic)
            current_page_num = request.GET.get('page', 1)
            # 分页,记住这里
            val = request.GET.get('q')
            field = request.GET.get('field')
            if val and field:
                q = Q()
                q.children.append((field + "__contains", val), )
                customers_list = Customer.objects.filter(q)

            pagination = Pagination(current_page_num, customers_list.count(), request)
            customers_list = customers_list[pagination.start:pagination.end]
            return render(request, "customers/customer_all.html", locals())
        else:
            from app01.models import UserInfo
            user_obj = UserInfo.objects.filter(user=request.session.get('user_id')).first()
            from app01.models import UserInfo
            print(request.session.get('user_id'))
            lable = '我的客户'

            customers_list = Customer.objects.filter(consultant=user_obj.pk)
            # except Exception:
            #     customers_list = Customer.objects.filter(consultant=user_obj.pk)

        # search过滤
        val = request.GET.get('q')
        field = request.GET.get('field')
        if val and field:
            q = Q()
            q.children.append((field + "__contains", val), )
            customers_list = Customer.objects.filter(q)

        # if val:
        #     customers_list= Customer.objects.filter(Q(name__contains=val)|Q(qq__contains=val))

        current_page_num = request.GET.get('page', 1)
        # 分页,记住这里
        pagination = Pagination(current_page_num, customers_list.count(), request)
        customers_list = customers_list[pagination.start:pagination.end]
        path = request.path
        next = "?next=%s" % (path)
        return render(request, "customers/customer_list.html", locals())

    # 批量操作
    def post(self, request):
        print(request.POST)
        func_str = request.POST.get('action')
        # 注意用getlist
        select_id = request.POST.getlist('select_id')
        if not hasattr(self, func_str):
            return HttpResponse('输入错误')
        else:
            func = getattr(self, func_str)
            print(func)
            # 一个queryset
            customer_queryset = Customer.objects.filter(pk__in=select_id)
            ret = func(request, customer_queryset)
            # 如果有有返回值就返回自己的,如果没有就重定向,因为下面限制公户转私户的时候,两个人如果同时打开界面,如果相中一个人,手慢的会有一个返回值
            if ret:
                return ret

            return redirect(request.path)

            # 从哪里改的就回哪里去

    # 批量删除
    def patch_delete(self, request, customer_queryset):
        customer_queryset.delete()

    # 公户转私户
    def patch_change(self, request, customer_queryset):
        # 如果有销售就不要添加了,否则两个人同时打开界面,谁后添加就是谁的客户于理不和
        ret = customer_queryset.filter(consultant__isnull=True)
        if ret:
            return HttpResponse('手数慢了')
        else:
            customer_queryset.update(consultant=request.user)

    # 私户转公户
    def patch_change_public(self, request, customer_queryset):
        customer_queryset.update(consultant=None)


from app01.forms import customers, recoder, Userform, eroll


class AddCustomerView(View):
    def get(self, request):
        form = customers.CustomerModelForm()
        return render(request, "customers/addcustomer.html", {"form": form})

    def post(self, request):
        form = customers.CustomerModelForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, "customers/addcustomer.html", {"form": form})


class EditCustomerView(View):
    # def dispatch(self, request, *args, **kwargs):
    #     obj = Customer.objects.filter(pk=id)
    #     return obj
    def get(self, request, id):
        if request.path == reverse('editcustomers', args=(id,)):
            obj = Customer.objects.filter(pk=id).first()
            form = customers.CustomerModelForm(instance=obj)
            return render(request, "customers/editcustomer.html", {"form": form})
        else:
            Customer.objects.filter(pk=id).delete()
            return redirect(request.GET.get('next'))

    # def post(self,request):
    def post(self, request, id):

        obj = Customer.objects.filter(pk=id).first()
        form = customers.CustomerModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(request.GET.get('next'))
        else:
            return render(request, "customers/editcustomer.html", {"form": form})


# 优化,add edit 的 区别在于有没有参数, instance 里有没有对象
# class EditAddCustomerView(View):
#     #如果不加单调删除,可以优化将
#     def get(self,request,id=None):
#         obj = Customer.objects.filter(pk=id).first()
#         form = CustomerModelForm(instance=obj)
#         return render(request, "edit_add_customer.html", {"form": form,"obj":obj})
#     def post(self,request,id=None):
#         obj = Customer.objects.filter(pk=id).first()
#         form = CustomerModelForm(request.POST, instance=obj)
#         if form.is_valid():
#             form.save()
#             return redirect(request.GET.get('next'))
#         else:
#             return render(request, "edit_add_customer.html", {"form": form,"obj":obj})


# 批量处理和展示在一起 处理完直接返回request.path
class RecoderCustomerView(View):
    def get(self, request):
        if request.path == reverse('recodercustomer'):
            lable = '我的客户跟进记录'
            recoder_list = ConsultRecord.objects.filter(consultant=request.user)
        elif request.path == reverse("recoderpublic"):
            lable = '好友客户跟进记录'
            recoder_list = ConsultRecord.objects.all()
        else:
            pk = request.GET.get('pk')
            lable = ''
            recoder_list = ConsultRecord.objects.filter(customer_id=pk)

        val = request.GET.get('q')
        field = request.GET.get('field')
        path = request.path
        next = "?next=%s" % (path)
        if field and val:
            q = Q()

            if field == "status" or field == 'name':
                q.children.append(('customer__' + field + "__contains", val), )

            #     ConsultRecord.objects.filter(customer__status__contains='studying')
            else:
                q.children.append((field, val), )
            recoder_list = ConsultRecord.objects.filter(q)
        current_page_num = request.GET.get('page', 1)
        pagination = Pagination(current_page_num, recoder_list.count(), request)
        recoder_list = recoder_list[pagination.start:pagination.end]
        print('ldkjsf', recoder_list)
        return render(request, 'customers/recoder.html',
                      {"recoder_list": recoder_list, 'lable': lable, "pagination": pagination, 'next': next})

    def post(self, request):
        func_str = request.POST.get('action')
        select_id = request.POST.getlist('select_id')
        print('哈哈', func_str, select_id)
        if not hasattr(self, func_str):
            return HttpResponse('输入错误')
        else:
            func = getattr(self, func_str)
            func(request, select_id)
            return redirect(request.path)

    def patch_delete(self, request, id):

        ConsultRecord.objects.filter(pk__in=id).delete()

    def patch_change_public(self, request, id):
        ret = ConsultRecord.objects.filter(pk__in=id).values("consultant__pk")
        ConsultRecord.objects.filter(pk__in=id).delete()


# 添加完从哪来的就去哪
class AddrecoderCustomer(View):
    def get(self, request):
        form = recoder.RecoderCustomerFrom()
        return render(request, 'customers/addrecoderr.html', {"form": form})

    def post(self, request):
        form = recoder.RecoderCustomerFrom(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.GET.get('next'))


class EditrecodrView(View):
    def get(self, request, id):
        print(request.path)
        if request.path == reverse('editrecoder', args=(id,)):
            # print("=========================")
            obj = ConsultRecord.objects.filter(pk=id).first()
            form = recoder.RecoderCustomerFrom(instance=obj)
            return render(request, "customers/editrecoderr.html", {"form": form})
        else:
            ConsultRecord.objects.filter(pk=id).delete()
            return redirect(request.GET.get('next'))

    def post(self, request, id):
        obj = ConsultRecord.objects.filter(pk=id).first()
        form = recoder.RecoderCustomerFrom(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        return redirect(request.GET.get('next'))


# 报名表的增删改查
class EnrollmentView(View):
    def get(self, request):
        eroll_list = Enrollment.objects.all()
        print(eroll_list)

        val = request.GET.get('q')
        field = request.GET.get('field')
        if val and field:
            q = Q()
            q.children.append((field + "__contains", val), )
            eroll_list = Enrollment.objects.filter(q)

        # if val:
        #     customers_list= Customer.objects.filter(Q(name__contains=val)|Q(qq__contains=val))

        current_page_num = request.GET.get('page', 1)
        # 分页,记住这里
        pagination = Pagination(current_page_num, eroll_list.count(), request)

        eroll_list = eroll_list[pagination.start:pagination.end]

        return render(request, "enrollment.html", locals())

    def post(self, request):
        func_str = request.POST.get('action')
        ret = request.POST.getlist('select_id')
        print(func_str, ret)
        if hasattr(self, func_str):
            func = getattr(self, func_str)
            func(request, ret)
        else:
            return HttpResponse('输入错误')
        return redirect(request.path)

    def patch_delete(self, request, id):
        Enrollment.objects.filter(pk__in=id).delete()


class EditAddenrollment(View):
    def get(self, request, id=None):
        obj = Enrollment.objects.filter(pk=id).first()
        form = eroll.ErollmentForm(instance=obj)
        return render(request, 'editaddenrollment.html', {"form": form, "obj": obj})

    def post(self, request, id=None):
        obj = Enrollment.objects.filter(pk=id).first()
        form = eroll.ErollmentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        else:
            return redirect(request.path)
        return redirect(reverse("enroll"))



class ClassStudyRecordView(View):
    def get(self, request, id=None):
        if request.path == reverse("classsturecoder"):
            ClassStudyRecord_list = ClassStudyRecord.objects.all()
            current_page_num = request.GET.get('page', 1)
            # 分页,记住这里
            pagination = Pagination(current_page_num, ClassStudyRecord_list.count(), request)
            ClassStudyRecord_list = ClassStudyRecord_list[pagination.start:pagination.end]
            path = request.GET.get('path')
            return render(request, "students/classstudentrecorder.html",
                          {"ClassStudyRecord_list": ClassStudyRecord_list, "pagination": pagination})

    def post(self, request):
        func_str = request.POST.get("action")
        id_list = request.POST.getlist("select_id")
        if hasattr(self, func_str):
            func = getattr(self, func_str)
            ret = func(id_list)
            if ret:
                return ret
            # 返回继续查看界面
            return self.get(request)

    def patch_delete(self, queryset):
        queryset.delete()

    # 批量创建学习记录
    def patch_create(self, selected_pk_list):
        # print(111)
        try:
            # print(selected_pk_list)
            # 批量创键学习记录
            for classstudy_pk in selected_pk_list:
                print(classstudy_pk)
                # 从班级学习记录表里过滤出对应班级的学习记录对象
                class_study_record_obj = ClassStudyRecord.objects.filter(pk=classstudy_pk).first()
                # print(class_study_record_obj)
                # 班级记录对象与学生 并没有直接关联,所以需要找班级记录表所关联的班级,班级里面的所有学生
                student_list = class_study_record_obj.class_obj.student_set.all()
                print("=====================",student_list)
                for student in student_list:
                    StudentStudyRecord.objects.create(student=student, classstudyrecord=class_study_record_obj)
        except Exception as e:
            pass


from app01.forms import classstudyrecorder


class ClassStudyRecordAdd_Edit(View):
    def get(self, request, id=None):
        # print(request.path)
        obj = ClassStudyRecord.objects.filter(pk=id).first()
        if request.path == reverse("classstuadd") or request.path == reverse("classstuedit", args=(id,)):
            forms = classstudyrecorder.ClassStudyRecordForm(instance=obj)
            return render(request, "students/classrecoderadd_edit.html", {"forms": forms})
        elif request.path == reverse("classstudel", args=(id,)):
            obj.delete()
            return redirect(reverse("classsturecoder"))

    def post(self, request, id=None):
        obj = ClassStudyRecord.objects.filter(pk=id).first()
        forms = classstudyrecorder.ClassStudyRecordForm(request.POST, instance=obj)
        if forms.is_valid():
            forms.save()
            return redirect(reverse("classsturecoder"))
        else:
            return render(request, "students/classrecoderadd_edit.html", {"forms": forms})


# 学生学习记录表的增删改查
class StudentStudyRecordView(View):
    def get(self, request):
        student_list = StudentStudyRecord.objects.all()
        current_page_num = request.GET.get('page', 1)
        # 分页,记住这里
        pagination = Pagination(current_page_num, student_list.count(), request)

        student_list = student_list[pagination.start:pagination.end]

        return render(request, "students/studentsturecorder.html",
                      {"student_list": student_list, "pagination": pagination})


# 学生学习记录表的增删改查
from app01.forms import studentstudy


class StudentStudyRecordAdd_Edit(View):
    def get(self, request, id=None):
        # print(request.path)
        obj = StudentStudyRecord.objects.filter(pk=id).first()
        if request.path == reverse("studenttuadd") or request.path == reverse("studentstuedit", args=(id,)):

            forms = studentstudy.StudentStudyRecordForm(instance=obj)
            return render(request, "students/studentrecoderadd_edit.html", {"forms": forms})
        elif request.path == reverse("studentstudel", args=(id,)):
            obj.delete()
            return redirect(reverse("studentsturecoder"))

    def post(self, request, id=None):
        obj = StudentStudyRecord.objects.filter(pk=id).first()
        forms = studentstudy.StudentStudyRecordForm(request.POST, instance=obj)
        if forms.is_valid():
            forms.save()
            return redirect(reverse("studentsturecoder"))
        else:
            return HttpResponse('No')
            # render(request,"studentrecoderadd_edit.html",{"forms":forms})


#  查询今天的销售,昨天的
#  我当是写了好多路由都要把自己逼疯了,老师的方法极好
from django.db.models import Count,DateField

class TongJiView(View):
    def today(self):
        import datetime
        # 取得年月日
        today = datetime.datetime.now().date()  # datetime.datetime.now() 年月日 时分秒对象, date()只取日期
        # 今天成交的所有客户
        customer_list = Customer.objects.filter(baoming_date=today)
        # 查询每一个销售的名字,以及今天的对应成单量, 你得查数所有的销售,因为有的销售没有成单量你也应该显示
        # UserInfo.objects.filter(depart_id=2, customers__baoming_date=today).annotate(c=Count('customers')).values('name','c')

        # 因为里面有个别名,要不然反向查询按照表名小写_set.all()
        from django.db.models import Q
        # q = Q()
        # q1 = Q()
        # q2 = Q()
        # q.connector = 'or'
        # q.children.append(("customers__baoming_date",today))
        # q.children.append(("customers__baoming_date", None))
        # q1.children.append(("depart_id" ,2))
        # q2.add(q,q1)
        from django.db import connection
        from django.db.models import Max, Case, When, F
        # ret = UserInfo.objects.annotate(
        #     f=Count(Case(When(depart_id=2,customers__baoming_date=today, then=F('customers__baoming_date'))))).values_list("username", "f")
        ret = UserInfo.objects.filter(depart_id=2).annotate(
            c=Count(Case(When(depart_id=2, customers__baoming_date=today, then=F('customers'))))).values_list("username", "c")
        #ret = UserInfo.objects.extra(select=["customers__baoming_date='2019-03-16' OR  customers__baoming_date='None'","depart_id='2'"])
        # ret = UserInfo.objects.filter(depart=2,customers__baoming_date=today).annotate(
        #      c=Count("customers")).values_list("username", "c")
        # ret1 = UserInfo.objects.filter(depart_id=2).values_list("username")
        # ret1 = [[item[0],0] for item in list(ret1)]
        ret = [[item[0], item[1]] for item in list(ret)]
        # ret.extend(ret1)
        print(ret,"==============",)
        print(connection.queries)
        return {"customer_list": customer_list, "ret": ret}

    def yesterday(self):
        import datetime
        # 取得年月日
        yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
        # print(yesterday)
        customer_list = Customer.objects.filter(baoming_date=yesterday)
        # 因为里面有个别名,要不然反向查询按照表名小写_set.all()
        # 过滤出每个销售的成交量

        ret = UserInfo.objects.filter(depart=2, customers__baoming_date=yesterday).annotate(
            c=Count("customers")).values_list("username", "c")
        # print(ret)
        ret = [[item[0], item[1]] for item in list(ret)]
        return {"customer_list": customer_list, "ret": ret}

    def week(self):
        import datetime
        # 取得年月日
        today = datetime.datetime.now().date()
        week_today = datetime.datetime.now().date() - datetime.timedelta(weeks=1)
        customer_list = Customer.objects.filter(baoming_date__gte=week_today, baoming_date__lte=today, )
        # 因为里面有个别名,要不然反向查询按照表名小写_set.all()
        ret = UserInfo.objects.filter(depart=2, customers__baoming_date__gte=week_today,
                                      customers__baoming_date__lte=today).annotate(
            c=Count("customers")).values_list("username", "c")
        ret = [[item[0], item[1]] for item in list(ret)]
        return {"customer_list": customer_list, "ret": ret}

    def recent_month(self):
        import datetime
        # 取得年月日
        today = datetime.datetime.now().date()
        recent_month = datetime.datetime.now().date() - datetime.timedelta(weeks=4)
        customer_list = Customer.objects.filter(baoming_date__gte=recent_month, baoming_date__lte=today)
        # 因为里面有个别名,要不然反向查询按照表名小写_set.all()
        ret = UserInfo.objects.filter(depart=2, customers__baoming_date__gte=recent_month,
                                      customers__baoming_date__lte=today).annotate(
            c=Count("customers")).values_list("username", "c")
        ret = [[item[0], item[1]] for item in list(ret)]
        return {"customer_list": customer_list, "ret": ret}

    def get(self, request):
        date = request.GET.get('date', "today") # 如果取不到默认今天的
        if hasattr(self, date):
            context = getattr(self, date)()  # 函数名() 直接调用
        return render(request, "customers/tongji.html", context)

# datetime.datetime    年月日,时分秒
# datetime.date        年月日
# datetime.time        时分秒
# datetime.timedelta   时差
# 批量录入成绩
class RecordScoreView2(View):

    def get(self, request, class_study_record_id):
        class_study_record_obj = ClassStudyRecord.objects.get(pk=class_study_record_id)
        # print(class_study_record_obj)
        student_study_record_list = class_study_record_obj.studentstudyrecord_set.all()
        # print("student_study_record_list",student_study_record_list)
        score_choices = StudentStudyRecord.score_choices
        return render(request, "students/scoreshow.html", locals())

    def post(self, request, class_study_record_id):

        print(request.POST)
        #
        # < QueryDict: {'csrfmiddlewaretoken': ['nJ0h1ldSmTXtEKSjN2UeO4BCztp1ZAqaRwjVQotjS7iMx4NAF6uuW1U25lcaFba3'],
        #               'score_23': ['70'], 'homework_note_23': ['142'], 'score_31': ['70'], 'homework_note_31': ['45'],
        #               'score_35': ['70'], 'homework_note_35': ['\r\n47\r\n']} >
        data_dict = {}

        #  重点
        for key, val in request.POST.items():
            print(key, val)
            if key == "csrfmiddlewaretoken":
                continue
            field, pk = key.rsplit("_", 1)  # 以右面为分,分一次
            # 这样写不行,因为拿不出批语
            # StudentStudyRecord.objects.filter(pk=pk).update(score=val,)
            if pk not in data_dict:
                data_dict[pk] = {
                    field: val
                }
            else:
                data_dict[pk][field] = val

        print(data_dict)
        for pk, data in data_dict.items():
            StudentStudyRecord.objects.filter(pk=pk).update(**data)

        # StudentStudyRecord.objects.filter(pk=pk).update(**{field:val})

        return redirect(request.path)
from django import  forms
class Recorder(forms.ModelForm):
    class Meta:
        model=StudentStudyRecord
        fields = ["score", "homework_note"]  # 如果是__all__ 校验所有字段
from django.forms.models import modelformset_factory
class RecordScoreView(View):
    # extra=1 额外添加一个
    def get(self, request, class_study_record_id):
        modelformset = modelformset_factory(model=StudentStudyRecord,form=Recorder,extra=0)
        queryset = StudentStudyRecord.objects.filter(classstudyrecord=class_study_record_id)
        formset = modelformset(queryset=queryset)
        return render(request, "students/scoreshow.html", locals())

    def post(self, request,class_study_record_id):
        model_formset_cls = modelformset_factory(model=StudentStudyRecord, form=Recorder, extra=0)
        print("request.POST",request.POST)
        formset=model_formset_cls(request.POST)
        if formset.is_valid():
            formset.save()

        print(formset.errors)

        return redirect(request.path)

