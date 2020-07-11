from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class JinZhiMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        print(request.path)
        white_list =  ['/index/','/login/','/reg/',"/get_valid_img/","/admin/*"]
        current_url = request.path_info

        # 白名单的判断
        import re
        for i in white_list:
            if re.match(i, current_url):
                return
        if not request.user.is_authenticated:
            return redirect('/login/')
# 全局的settings
from django.conf import settings
# 用户的settings  优先级高先去用户里找
from Crm import  settings
# class Curre
# settings.CU)