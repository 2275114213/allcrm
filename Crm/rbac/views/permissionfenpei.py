from rbac.models import Permission,Role,User1
from django.shortcuts import reverse,render,redirect
# 权限分配
def distribute_permissions(request):
    uid = request.GET.get('uid')
    user = User1.objects.filter(id=uid)
    rid = request.GET.get('rid')

    if request.method == "POST" and request.POST.get('postType') == 'role':
        l = request.POST.getlist("roles")
        user.first().roles.set(l)

    if request.method == "POST" and request.POST.get('postType') == 'permission':
        l = request.POST.getlist("permissions_id")
        Role.objects.filter(pk=rid).first().permissions.set(l)

    # 所有用户
    user_list = User1.objects.all()
    # user_has_roles = user.values('id', 'roles')
    role_list = Role.objects.all()
    # print("uid", uid)
    if uid:
        role_id_list = User1.objects.get(pk=uid).roles.all()
        print("role_id_list", role_id_list)
        role_id_list = [item[0] for item in role_id_list]

        if rid:
            per_id_list = Role.objects.filter(pk=rid).values_list("permissions__pk").distinct()
        else:
            per_id_list = User1.objects.get(pk=uid).roles.values_list("permissions__pk").distinct()
        per_id_list = [item[0] for item in per_id_list]
        # print("per_id_list", per_id_list)
    else:
        if rid:
            per_id_list = Role.objects.filter(pk=rid).values_list("permissions__pk").distinct()
            per_id_list = [item[0] for item in per_id_list]

    return render(request, 'distribute_permissions.html', locals())

# 权限处理ajax 请求的
from django.http import JsonResponse
def permissions_tree(self):
    permission_list = Permission.objects.values('pk',"title","url","menu__title","menu__pk","pid")
    return JsonResponse(list(permission_list), safe=False)



