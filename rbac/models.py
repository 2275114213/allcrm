from django.db import models

# Create your models here.
class User1(models.Model):
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    roles = models.ManyToManyField("Role")
class Role(models.Model):
    title=models.CharField(max_length=32)
    permissions = models.ManyToManyField("Permission")
    def __str__(self):
        return self.title

# 一个菜单下可以有多个权限,但是一个权限只能属于一个菜单
# 所以创建一对多的关系
class Menu(models.Model):
    title = models.CharField(max_length=32)
    icon = models.CharField(max_length=32, verbose_name='图标', null=True, blank=True)
class Permission(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32)
    pid = models.ForeignKey("self",on_delete=models.CASCADE,null = True,verbose_name='父权限')
    # is_menu = models.BooleanField(max_length=32,default=False)
    # icon = models.CharField(max_length=32,null=True,blank=True)
    #这个需要加上不然选权限的时候看的还是对象
    def __str__(self):
        return self.title