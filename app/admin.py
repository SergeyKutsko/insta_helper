from django.contrib import admin
from django import forms
from .models import InstagramUser, Limit, Template, SystemSetting, CustomUser


@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display = ['user']


@admin.register(InstagramUser)
class InstagramUserAdmin(admin.ModelAdmin):
    list_display = ['login', 'age', 'message', 'user']
    search_fields = ['login', ]


@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    list_display = ['name', 'limit', ]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', ]


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', ]

