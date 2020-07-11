from rbac.models import Role
def initial_session(request,user):

    # 这是菜单权限
    permissions = Role.objects.filter(user1=user).values('permissions__url',
                                                        "permissions__pid",
                                                        "permissions__pk",
                                                        'permissions__title',
                                                        "permissions__name",
                                                        "permissions__menu__pk",
                                                        "permissions__menu__title",
                                                        "permissions__menu__icon").distinct()
    # print("permissions=========================",permissions)
    # 获取权限列表
    permissions_list = []
    permissions_name = []

    permissions_menu_dict = {}
    for reg in permissions:

        # reg 是字典
        # 注入权限列表
        permissions_list.append({
            "url":reg["permissions__url"],
            "id":reg["permissions__pk"],
            "pid":reg["permissions__pid"],
            "title":reg["permissions__title"],
        })
        permissions_name.append(reg["permissions__name"])


        # 注入菜单列表
        menu_pk = reg["permissions__menu__pk"]
        if menu_pk:

            if menu_pk not in permissions_menu_dict:
                permissions_menu_dict[menu_pk] = {
                 'menu_title':reg["permissions__menu__title"],
                  "menu_icon":reg["permissions__menu__icon"],
                    "menu_pk":reg["permissions__menu__pk"],
                  "children":[
                                  {"title":reg["permissions__title"],
                                          'url':reg["permissions__url"],
                                          'id':reg["permissions__pk"],
                                   }

                                          ]
                                                 }


            # if menu_pk not in permissions_menu_dict:
            #
            #     permissions_menu_dict[menu_pk] = {
            #         "menu_title": reg["permissions__menu__title"],
            #         "menu_icon": reg["permissions__menu__icon"],
            #         "children": [
            #             {
            #                 "title": reg["permissions__title"],
            #                 "url": reg["permissions__url"],
            #             }
            #         ],
            #
            #     }
            else:
                permissions_menu_dict[menu_pk]["children"].append( {"title":reg["permissions__title"],
                                          'url':reg["permissions__url"],
                                                                    'id': reg["permissions__pk"],}
)
    # print("permissions_list",permissions_list)
    request.session["username"]  = user.name
    request.session['permissions__list'] = permissions_list
    request.session["permission__name"] = permissions_name
    request.session["permissions_menu_dict"] = permissions_menu_dict
    # print('haha',permissions_menu_dict)
#