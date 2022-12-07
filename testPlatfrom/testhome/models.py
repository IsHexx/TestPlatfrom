from django.db import models
from django.utils import timezone


class Home(models.Model):
    """测试数据汇总"""
    data_date = models.CharField(max_length=20)
    all = models.CharField(max_length=8)
    allpass = models.CharField(max_length=8)
    allfile = models.CharField(max_length=8)
    allbug = models.CharField(max_length=8)
    uiall = models.CharField(max_length=8)
    uipass = models.CharField(max_length=8)
    uifile = models.CharField(max_length=8)
    uibug = models.CharField(max_length=8)
    apiall = models.CharField(max_length=8)
    apipass = models.CharField(max_length=8)
    apifile = models.CharField(max_length=8)
    apibug = models.CharField(max_length=8)

    """
    * Python3格式化显示结果,如果是Python2的话就使用__unicode__方法
    """
    def __str__(self):
        return self.all


class PageModule(models.Model):
    """
    * 页面模块
    * 在Django中,如果创建Module时不指定id,Django会自动自定一个id
    * 如果自定义Id自增会与Django定义的Id冲突
    """
    # page_id = models.AutoField(primary_key=True,  help_text='页面模块id')
    name = models.CharField(max_length=20, help_text='页面模块名称')
    parent_id = models.CharField(max_length=8, help_text='父模块id')
    project_id = models.CharField(max_length=50, null=True, help_text='所属项目id')
    update_user = models.CharField(max_length=8, null=True, help_text='更新人')
    create_user = models.CharField(max_length=8, null=True, help_text='创建人')
    create_time = models.DateTimeField(default=timezone.now, help_text='创建时间')
    update_time = models.DateTimeField(default=timezone.now, help_text='更新时间')

    """
        @ Python3格式化显示结果,如果是Python2的话就使用__unicode__方法
    """
    def __str__(self):
        return self.name


class ElementModule(models.Model):
    """
    * 元素信息
    * 在Django中,如果创建Module时不指定id,Django会自动自定一个id
    * 如果自定义Id自增会与Django定义的Id冲突
    """
    # element_id = models.AutoField(primary_key=True,  help_text='元素id')
    # num = models.CharField(max_length=10, help_text='编号')
    name = models.CharField(max_length=20, help_text='元素名称')
    module_id = models.CharField(max_length=8, help_text='所属模块id')
    project_id = models.CharField(max_length=50, null=True, help_text='所属项目id')
    by = models.CharField(max_length=20,  help_text='定位方式')
    expression = models.CharField(max_length=200, help_text='元素表达式')
    element_description = models.CharField(max_length=200, null=True, help_text='元素描述')
    update_user = models.CharField(max_length=8, null=True, help_text='更新人')
    create_user = models.CharField(max_length=8, null=True, help_text='创建人')
    create_time = models.DateTimeField(default=timezone.now, help_text='创建时间')
    update_time = models.DateTimeField(default=timezone.now, help_text='更新时间')
    status = models.CharField(max_length=8, default=1, help_text='元素在用状态')

    """
    * Python3格式化显示结果,如果是Python2的话就使用__unicode__方法
    """
    def __str__(self):
        return self.name
