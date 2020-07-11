import re
from rbac.models import Permission
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
class PermissionMideeleWare(MiddlewareMixin):
    def process_request(self,request):
        current_path = request.path

        #白名单  /admin/加了也不行  因为admin跳转的是/admin/login/登录页面
        # if request.path in ['/login/','/admin/']:
        #     return None
        # #检验是否登录
        # user = request.session.get('user_id')
        # if not user:
        #
        #     return redirect('/login/')
        for ret in ['/login/','/admin/*','/permissions_tree/','/get_valid_img/','/index/','/register/','/reg/']:
            i = re.search(ret,current_path)
            request.showpid = ''
            request.breadcrumb = [
                {
                    "title": "首页",
                    "url": "/index/"
                },
            ]
            if i:
                return None

        # #检验是否登录
        user = request.session.get('user_id')
        if not user:

            return redirect('/login/')
        #检验权限

        #这么写里面的正则匹配有问题里面的(\d+ )是字符串,
        # if current_path not in request.session['permissions__url']:
        #     return redirect('/login/')
        # return None
        #所以需要for 循环
        # 路径导航列表:
        request.breadcrumb = [
            {
                "title": "首页",
                "url": "/index/"
            },
        ]
        for item in request.session.get('permissions__list'):
            # re.search('匹配规则',"匹配字符串")
            # 此处匹配有问题,如('orders/,'orders/edit/2')    可以匹配上
            #                ('orders','orders/delete/2')   都可已匹配上
            i = '^%s$'%item["url"]
            ret = re.search(i,current_path)
            # print(i)
            if ret:
                if item['pid']:
                    request.showpid = item['pid']
                    ppermission = Permission.objects.filter(pk=item["pid"]).first()
                    request.breadcrumb.extend(
                        [{
                            "title": ppermission.title,
                            "url": ppermission.url,
                        }, {
                            "title": item["title"],
                            "url": request.path
                        },  # 子权限字典
                        ]

                    )
                else:
                    request.showpid = item["id"]
                    request.breadcrumb.append(
                        {
                            "title": item["title"],
                            "url": item["url"]
                        }
                    )

                return None
        # 如果都循环完还没匹配上就是没有呢
        return HttpResponse('无权访问')
