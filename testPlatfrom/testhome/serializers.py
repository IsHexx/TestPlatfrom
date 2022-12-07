"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@Project : testPlatfromvue
@File : serializers.py
@Author : 细雨寻海
@Time : 2022/10/8 8:55
@Motto:Don't ever let somebody tell you you can't do something
"""
from rest_framework import serializers
from testhome.models import Home, PageModule, ElementModule


# 父类变成了ModelSerializer
class TestHomeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = '__all__'


class PageDataSerializer(serializers.ModelSerializer):
    # children = serializers.SerializerMethodField()
    class Meta:
        model = PageModule
        fields = ("id",
                  "name",
                  "parent_id",
                  "project_id",
                  "update_user",
                  "create_user",
                  "create_time",
                  "update_time"
                  )

    # def get_children(self, obj):
    #     """
    #     # SerializerMethodFiel是一个read-only字段
    #     # 当不指定其method_name时，默认为get_<field_name>
    #     # 如果使用ModelSerializer并指定字段时，要包含此时定义的字段
    #     # 函数命名方式固定为：get_ + 序列化的变量名
    #     :param PageDataSerializer:
    #     :return: 外键关联查询的字段
    #     """
    #     return obj.children


class ExternalAssociationElementSerializer(serializers.ModelSerializer):
    module_name = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = ElementModule
        fields = ('id',
                  'name',
                  'module_id',
                  'project_id',
                  'by',
                  'expression',
                  'element_description',
                  'update_user',
                  'create_user',
                  'create_time',
                  'update_time',
                  'status',
                  'module_name',
                  'total')

    def get_module_name(self, PageDataSerializer):
        """
        # 此方法只针对无外键的字段有效,如果查询有外键的字段会报错
        # 函数命名方式固定为：get_ + 序列化的变量名
        :param PageDataSerializer:
        :return: 外键关联查询的字段
        """
        return PageDataSerializer.module_name

    def get_total(self, obj):
        """
        # 此方法只针对无外键的字段有效,如果查询有外键的字段会报错
        # 函数命名方式固定为：get_ + 序列化的变量名
        :param PageDataSerializer:
        :return: 外键关联查询的字段
        """
        return obj.total


class ElementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementModule
        fields = "__all__"
