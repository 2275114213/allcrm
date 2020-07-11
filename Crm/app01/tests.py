from django.test import TestCase

# Create your tests here.
dic = {"今天":"haha","明天":"hehe"}
for item in dic:
    print(item)
    # 只有键值
    # 今天
    # 明天
for item in dic.values():
    print(item)
# haha
# hehe
for item,val in dic.items():
    print(item,val)
    # 今天 haha
    # 明天 hehe

# 列表推导式 循环网列表里面加东西
lis = [[i,j] for i,j in dic.items()]
print(lis)
# [['今天', 'haha'], ['明天', 'hehe']]