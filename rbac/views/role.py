from django.shortcuts import redirect,render,HttpResponse,reverse
from rbac.models import Role
from rbac.forms import roleForm
def role(request):
    if  request.method == "GET":
        role_list = Role.objects.all()
        return render(request,"role.html",{"role_list":role_list})
def role_add_edit(request,id = None):
    if request.method == "GET":
        obj = Role.objects.filter(pk = id).first()
        role_list = roleForm.RoleForm(instance= obj)
        return render(request, "role_add_edit.html", {"role_list":role_list})
    else:
        obj = Role.objects.filter(pk = id).first()
        form =  roleForm.RoleForm(request.POST,instance = obj)
        if form.is_valid():
            form.save()
            return redirect("/role/list/")
        else:
            return render(request,"role_add_edit.html")
def role_del(request,id):
   Role.objects.filter(pk=id).delete()
   return redirect("/role/list/")

