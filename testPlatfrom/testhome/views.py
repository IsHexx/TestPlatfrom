import json

from django.core.paginator import Page, Paginator
from django.db.models import Q, Value, CharField
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from testhome import serializers
from rest_framework import generics, viewsets
from testhome.models import Home, PageModule, ElementModule
from testhome.serializers import (
    TestHomeDataSerializer,
    PageDataSerializer,
    ElementDataSerializer, ExternalAssociationElementSerializer,
)

# 引入redirect重定向模块
from django.shortcuts import render, redirect

# 引入HttpResponse
from django.http import HttpResponse

# 引入User模型
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def testhome_data(request):
    articles = Home.objects.all()
    serializer = TestHomeDataSerializer(articles, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET", "POST"])
def element_list(request):
    # if request.method == "GET":
    #     element = ElementModule.objects.all()
    #     serializer = ElementDataSerializer(element, many=True)
    #     return Response(serializer.data)

    if request.method == "POST":
        json_str = request.body  # 属性获取最原始的请求体数据
        json_dict = json.loads(json_str)  # 将原始数据转成字典格式
        if "id" in json_dict:
            id = json_dict['id']  # 获取数据
        else:
            id = ""

        if id != "":
            element = ElementModule.objects.get(id=id)
            serializer = ElementDataSerializer(instance=element, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = ElementDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def element_list_push(request, page, pagesize):
    """
    1. 初始化元素列表
    2. 根据moudle_id查询元素
    3. 根据id/name查询元素
    :param request:
    :return:
    """
    if request.method == "POST":

        json_str = request.body  # 属性获取最原始的请求体数据
        json_dict = json.loads(json_str)  # 将原始数据转成字典格式
        # print(json_dict)
        element = ""
        condition = json_dict['condition']
        module_id = json_dict['module_id']

        if module_id != "" and condition != "":
            total = ElementModule.objects.filter((Q(module_id=module_id) & Q(id=condition)) |
                                                 (Q(module_id=module_id) & Q(name=condition))).count()
            element = ElementModule.objects.filter((Q(module_id=module_id) & Q(id=condition)) |
                                                   (Q(module_id=module_id) & Q(name=condition))).extra(
                select={'module_name': 'SELECT B.name FROM testhome_pagemodule B where B.id = module_id',
                        'total': total}).order_by('id')
        elif module_id != "":
            total = ElementModule.objects.filter(module_id=module_id).count()
            element = ElementModule.objects.filter(module_id=module_id).extra(
                select={'module_name': 'SELECT B.name FROM testhome_pagemodule B where B.id = module_id',
                        'total': total}).order_by('id')
        elif condition != "":
            total = ElementModule.objects.filter(Q(id=condition) | Q(name=condition)).count()
            element = ElementModule.objects.filter(Q(id=condition) | Q(name=condition)).extra(
                select={'module_name': 'SELECT B.name FROM testhome_pagemodule B where B.id = module_id',
                        'total': total}).order_by('id')
        else:
            element = ElementModule.objects.all().extra(
                select={'module_name': 'SELECT B.name FROM testhome_pagemodule B where B.id = module_id',
                        'total': 'SELECT count(1) FROM testhome_elementmodule '}).order_by('id')

        # for item in element:
        #     print(item.__dict__)
        element = Paginator(element, pagesize)
        element = element.get_page(page)

        serializer = ExternalAssociationElementSerializer(element, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        json_str = request.body  # 属性获取最原始的请求体数据
        json_dict = json.loads(json_str)  # 将原始数据转成字典格式
        return Response("接口传参错误")


@api_view(["GET", "POST"])
def element_delete(request):
    """
    删除元素
    :param request:
    :return:
    """
    if request.method == "POST":
        json_str = request.body  # 属性获取最原始的请求体数据
        json_dict = json.loads(json_str)  # 将原始数据转成字典格式
        # print("request_body的值为{0}".format(json_dict))
        if "id" in json_dict:
            id = json_dict['id']  # 获取数据
        else:
            id = None
        if id is not None:
            ElementModule.objects.filter(id=id).delete()
        else:
            return Response({'msg': '传参有误'})
        return Response("删除成功", status=status.HTTP_201_CREATED)
    else:
        return Response("删除失败")


@api_view(["GET", "POST"])
def get_page_list(request):
    group_list = []
    # 一次性读取所有页面信息
    group_object_list = PageModule.objects.all()
    for group in group_object_list:
        if group.parent_id != '0':
            continue
        group_dict = dep_to_dict(group)  # 将数据转换成对应的格式字典
        group_info = dept_menu(group_object_list, group_dict)
        group_list.append(group_info)
    # paginator = Paginator(group_list, 1)
    return Response(data=group_list, status=status.HTTP_200_OK)


# 通过递归实现获取当前菜单下面所有子菜单的信息
def dept_menu(group_list, dept_root):
    dept_info_list = []

    for group in group_list:
        # 获取当前部门的所有子部门
        if group.parent_id != str(dept_root['id']):
            continue
        # print(f"dept_root['parent_id'] value is :{dept_root['parent_id']}")
        dept_info = dep_to_dict(group)
        ms = dept_menu(group_list, dept_info)
        dept_info_list.append(ms)
    dept_root['children'] = dept_info_list
    return dept_root


def dep_to_dict(group):
    dept_info = {
        'id': group.id,
        'name': group.name,
        'parent_id': group.parent_id,
        'project_id': group.project_id,
        'update_user': group.update_user,
        'create_user': group.create_user,
        'create_time': group.create_time,
        'update_time': group.update_time,
        'children': []
    }
    return dept_info


@api_view(["POST"])
def page_list(request):
    """
    页面模块
    :param request: 请求方式
    :return: 序列化/反序列化数据
    """
    if request.method == "POST":
        serializer = PageDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def page_delete(request):
    """
    删除页面模块
    :param request:
    :param id:
    :return:
    """
    if request.method == "POST":
        json_str = request.body  # 属性获取最原始的请求体数据
        json_dict = json.loads(json_str)  # 将原始数据转成字典格式
        # print("request_body的值为{0}".format(json_dict))
        if "id" in json_dict:
            id = json_dict['id']  # 获取数据
        else:
            id = None
        page = PageModule.objects.get(id=id)
        page.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response("接口传参错误")
