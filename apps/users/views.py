# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm
from utils.email_send import send_email
from .models import EmailVerifyCode


class CustomBackend(ModelBackend):
    """
    在这里重写authenticate方法，实现自定义的校验功能，比如可以邮箱或用户名登陆
    """
    def authenticate(self, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        return render(request, 'index.html', {})


class ActiveUserView(View):
    """
    激活用户
    """
    def get(self, request, active_code):
        all_records = EmailVerifyCode.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                EmailVerifyCode.delete(record)
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    """
    用户注册
    """
    def get(self, request):
        return render(request, 'register.html', {})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        # 验证数据格式是否合法
        if register_form.is_valid():
            email = request.POST.get("email", "")
            # 验证邮箱好是否已被注册
            if User.objects.filter(email=email):
                return render(request, "register.html", {"register_form": register_form, "msg": "该邮箱已被注册"})
            pass_word = request.POST.get("passwd", "")
            user = User()
            user.email = email
            user.is_active = False
            user.password = make_password(pass_word)
            user.save()
            # 用户保存到数据库后，发送激活链接
            send_email(email, "register", 16)
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    """
    用户登陆
    """
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        # 验证数据格式是否合法
        if login_form.is_valid():

            email = request.POST.get("email", "")
            pass_word = request.POST.get("passwd", "")
            # 这里的authenticate方法实际调用的是上面CustomBackend类里的authenticate方法
            user = authenticate(email=email, password=pass_word)
            if user is not None:  # 用户名或密码是否正确
                if user.is_active:  # 用户是否处于激活状态
                    login(request, user)
                    # 注意这里需要重定向，因为直接跳转无法携带首页所需要的数据
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    """
    用户注销
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))



