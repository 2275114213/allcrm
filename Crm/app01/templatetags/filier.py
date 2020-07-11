from django.shortcuts import reverse
from django.template import Library

import urllib.parse
# ret = urllib.parse.urlencode(self.filter_dict)
register = Library()
@register.simple_tag()
def filter(ret,id,request):
    ret["consultant"]=id
    return urllib.parse.urlencode(ret)
#
#     # for i,j in reg.items():