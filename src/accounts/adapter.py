# -*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from allauth.account.adapter import get_adapter
from allauth.account.adapter import DefaultAccountAdapter

translate = {u'ą':'a', u'ć':'c', u'ę':'e', u'ł':'l', u'ń':'n', u'ó':'o', u'ś':'s', u'ż':'z', u'ź':'z'}

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

# class MyAccountAdapter(DefaultAccountAdapter):
#     def clean_username(self, username, shallow=False):
#         """
#         """
#         print("dupa")
#         print("before username", username)
#         username = replace_all(text=username, dic=translate)
#         print("after username", username)
#         return username