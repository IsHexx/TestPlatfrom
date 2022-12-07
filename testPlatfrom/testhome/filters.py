"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : testPlatfromvue
@File : filters.py
@Author : 细雨寻海
@Time : 2022/11/29 9:52
@Motto:Don't ever let somebody tell you you can't do something
"""

import django_filters

from testhome.serializers import ElementDataSerializer


class ElementListFilter(django_filters.FilterSet):
    class Meta:
        model = ElementDataSerializer
        fields = ['moudle_id', ]
