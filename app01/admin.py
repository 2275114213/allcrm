from django.contrib import admin

# Register your models here.
from app01.models import *
from rbac.models import User1,Menu,Permission,Role
admin.site.register(UserInfo)
admin.site.register(ClassList)
admin.site.register(Customer)
admin.site.register(Campuses)
admin.site.register(ConsultRecord)
admin.site.register(Enrollment)
admin.site.register(PaymentRecord)
admin.site.register(Permission)
admin.site.register(Menu)
admin.site.register(Role)
admin.site.register(User1)
admin.site.register(Student)
admin.site.register(ClassStudyRecord)
admin.site.register(StudentStudyRecord)







#
class IndexPromo(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # 更新或新增表中的数据时调用
        super().save_model(request, obj, form, change)
        from celery_tasks.email_tasks import genertate_static_index_html
        genertate_static_index_html.delay()

    def delete_model(self, request, obj):
        # 删除表中的数据时,调用
        super().delete_model(request, obj)
        from celery_tasks.email_tasks import genertate_static_index_html
        genertate_static_index_html.delay()


admin.site.register(Book,IndexPromo)






