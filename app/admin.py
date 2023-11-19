from django.contrib import admin
from django import forms
from .models import InstagramUser, Teg, Limit


@admin.register(Teg)
class TegAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(InstagramUser)
class InstagramUserAdmin(admin.ModelAdmin):
    list_display = ['login', 'password', 'name', 'second_name', 'main', 'follower', 'track', 'target', 'sum']
    list_editable = ['name', 'second_name', 'main', 'target', 'sum']
    list_filter = ['main', ]
    search_fields = ['login', 'name', 'second_name']


@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    list_display = ['name', 'limit']

