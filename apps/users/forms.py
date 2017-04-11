# -*- encoding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    """
    登陆表单验证
    名称和html页面的字段名称必须相同
    """
    email = forms.CharField(required=True, error_messages={'required': '用户名/邮箱不能为空'})
    passwd = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空',
                                                                          'min_length': '密码不能少于6位'})


class RegisterForm(forms.Form):
    """
    注册表单验证
    名称和html页面的字段名称必须相同
    """
    email = forms.EmailField(required=True)
    passwd = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空',
                                                                            'min_length': '密码不能少于6位'})