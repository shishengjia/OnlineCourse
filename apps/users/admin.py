from django.contrib import admin
from .models import EmailVerifyCode


class EmailVerifyCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type']


admin.site.register(EmailVerifyCode, EmailVerifyCodeAdmin)
