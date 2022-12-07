"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : testPlatfromvue
@File : forms.py
@Author : 细雨寻海
@Time : 2022/11/22 10:33
@Motto:Don't ever let somebody tell you you can't do something
"""
# 引入表单类
from django import forms
# 引入文章模型
from .models import PageModule


# # 增加模块的表单类
# class CreatePagePostForm(forms.ModelForm):
#     class Meta:
#         # 指明数据模型来源
#         model = PageModule
#         # 定义表单包含的字段
#         fields = ('name', 'parent_id')
#
#
# # 增加元素的表单类
# class CreateElementPostForm(forms.ModelForm):
#     class Meta:
#         # 指明数据模型来源
#         model = PageModule
#         # 定义表单包含的字段
#         fields = ('name', 'parent_id')
