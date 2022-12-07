"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : testPlatfromvue
@File : urls.py
@Author : 细雨寻海
@Time : 2022/10/8 8:59
@Motto:Don't ever let somebody tell you you can't do something
"""
from django.urls import path
from testhome import views

app_name = 'testhome'

urlpatterns = [
    path('', views.testhome_data, name='testhome_data'),
    path('pagelist', views.page_list, name='page_list'),
    path('getpagelist', views.get_page_list, name='get_page_list'),
    path('pagedelete', views.page_delete, name='page_delete'),
    path('elementlist', views.element_list, name='element_list'),
    path('elementlistpush/<int:page>/<int:pagesize>', views.element_list_push, name='element_list_push'),
    path('elementdelete', views.element_delete, name='element_delete'),
]