from django.shortcuts import reverse
from django.template import Library
register = Library()

#定义好的过滤器
@register.filter
def cal(x,y):
    return x*y
from django.utils.safestring import mark_safe





#标签过滤器;
@register.filter
def tag(val):
    return mark_safe("<a>%s</a>"%val)

@register.inclusion_tag("../../rbac/templates/bread.html")
def bread(request):
    # print("++++++++++++++++++++++",request.breadcrumb)
    return {"breadcrumb":request.breadcrumb}



# {% for foo in request.breadcrumb %}
#             <a href="{{ foo.url }}">{{ foo.title }}</a>
#             {% if not forloop.last %}
#             >
#             {% endif %}
#         {% endfor %}
# @register.inclusion_tag("../../rbac/templates/menu.html")
# def menu_list_styles(request):
#     permissions_menu_dict = request.session.get('permissions_menu_dict')
#
#     # for reg in permissions_menu_list:
#     #     print(reg)
#     #     import re
#     #     # [{'title': '查看订单', 'url': '/payment/', 'icon': 'fa-code-fork'},
#     #     #  {'title': '查看客户', 'url': '/customers/', 'icon': 'fa-connectdevelop'}]
#     #     ret = re.search("^{}$".format(reg["url"]), request.path)
#     #     print(ret)
#     #     if ret:
#     #         reg["class"] = "active"
#     return {"permissions_menu_dict":permissions_menu_dict}

# 这个ruturn  是直接将模板menu.html  渲染好变量直接给调用的地方,
# 自定义标签将数据和模板结合

import re
@register.inclusion_tag("../../rbac/templates/menu.html")
def path(request):
    permission_menu_dict = request.session.get("permissions_menu_dict")
    # print("permission_menu_dict", permission_menu_dict)

    for val in permission_menu_dict.values():
        for item in val["children"]:
            val["class"] = "hide"
            # print(type(item["id"]))
            # /payment/
            # /payment/edit/4/
            # ret=re.search("^{}$".format(item["url"]),request.path)
            # print(request.POST)

            if request.showpid == item["id"]:
                # print(1111)
                val["class"] = ""
                break


    # print("permission_menu_dict", permission_menu_dict)
    return {"permission_menu_dict": permission_menu_dict}

# [{'title':cdvn,"preice":455},
# {'title':ff,"preice":455},
#  {class:hahah}
#  ]



# 这个可通过判断来实现,但是麻烦,每个里都要写判断语句,所以定义了方法
# 而且给每个url起了别名,解决路径拿出来一个一个匹配的low做法
@register.filter
def showorhide(btn_url_name,request):
    permissions = request.session.get("permission__name")
    # print('娃哈哈',permissions)
    return btn_url_name in permissions



@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()

















