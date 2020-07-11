from django.shortcuts import redirect,render,reverse,HttpResponse
from rbac.models import  Menu
from rbac.models import Permission
from django.db.models import Q
from rbac.forms import  menuForms
def menu(request):
    all_menu = Menu.objects.all()

    mid = request.GET.get('mid')

    if mid:
        permission_query = Permission.objects.filter(Q(menu_id=mid) | Q(pid=mid))
    else:
        permission_query = Permission.objects.all()

    all_permission = permission_query.values('id', 'url', 'title', 'name', 'menu_id', 'pid', 'menu__title')

    all_permission_dict = {}

    for item in all_permission:
        menu_id = item.get('menu_id')
        if menu_id:
            item['children'] = []
            all_permission_dict[item['id']] = item

    for item in all_permission:
        pid = item.get('pid')

        if pid:
            all_permission_dict[pid]['children'].append(item)

    print(all_permission_dict)

    return render(request, 'menu_list.html',
                  {"all_menu": all_menu, 'all_permission_dict': all_permission_dict, 'mid': mid})


def menu_add_edit(request,id = None):
    if request.method == "GET":
        obj = Menu.objects.filter(pk = id).first()
        form = menuForms.MenuForm(instance=obj)
        return render(request,"menu_add_edit.html",{"form":form})
    else:
        obj = Menu.objects.filter(pk=id).first()
        form = menuForms.MenuForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect("/menu/list/")
        else:
            return render(request,"menu_add_edit.html")
def menu_del(request):
    pass