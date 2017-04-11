# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class EmailVerifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 记录是何种类型
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码"),
                                          ("update_email", "更新邮箱")), max_length=15, verbose_name="验证码类型")
    # datetime.now()返回model编译时的时间
    # datetime.now 返回model实例化时的时间
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    # 点击图片后的跳转地址
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    # 控制轮播图的顺序
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "轮播图片"
        verbose_name_plural = verbose_name

