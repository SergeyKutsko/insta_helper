from django.contrib import admin
from django import forms
from .models import InstagramUser, Teg, Limit, Income, UserID, Template


@admin.register(Teg)
class TegAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(InstagramUser)
class InstagramUserAdmin(admin.ModelAdmin):
    list_display = ['login', 'password', 'name', 'second_name', 'main', 'follower', 'track', 'target', ]
    list_editable = ['name', 'second_name', 'main', 'target',]
    list_filter = ['main', ]
    search_fields = ['login', 'name', 'second_name',]


@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    list_display = ['name', 'limit', ]


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['sum', 'currency', 'user', ]


@admin.register(UserID)
class UserIDAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'teg', ]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', ]

