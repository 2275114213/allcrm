from django.urls import path,re_path
from rbac.views import role,menu
from rbac.views import permissionfenpei
urlpatterns = [
path("role/list/",role.role),
re_path("role/edit/(\d+)/",role.role_add_edit,name="role_edit"),
re_path("role/add/",role.role_add_edit,name="role_add"),
re_path("role/del/(\d+)/",role.role_del,name="role_del"),
path('menu/list/',menu.menu,),
re_path('menu/edit/(\d+)/',menu.menu_add_edit,name = "menu_edit"),
path('menu/add/',menu.menu_add_edit,name = "menu_add"),
re_path('menu/del/(\d+)/',menu.menu_del,name = "menu_del"),
path('distribute/permissions/', permissionfenpei.distribute_permissions, name='distribute_permissions'),
# path('distribute/permissions2/', permissionfenpei.distribute_permissions2, name='distribute_permissions'),
path('permissions_tree/', permissionfenpei.permissions_tree, name='distribute_permissions'),
]