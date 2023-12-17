from django.contrib import admin
from .models import InstagramUser, Limit, Template, SystemSetting, UserId, ListName
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django import forms


@admin.register(InstagramUser)
class InstagramUserAdmin(admin.ModelAdmin):
    list_display = ['login', 'age', ]
    search_fields = ['login', ]

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)


@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    list_display = ['name', 'limit', 'description']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', ]

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', ]


class UserIdForm(forms.ModelForm):
    class Meta:
        model = UserId
        fields = ['url']


@admin.register(UserId)
class UserIdAdmin(ImportExportModelAdmin):
    form = UserIdForm

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['url', 'page_id']

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['url', 'page_id', 'user'
                                                 ]}),

            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['url',
                                     ]}),

            ]
        return fieldsets

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        try:
            super(UserIdAdmin, self).save_model(request, obj, form, change)
        except IntegrityError as e:
            self.message_user(request, f"Помилка збереження: Таке значення вже є в базі данних {e}", level='ERROR')


@admin.register(ListName)
class ListNameAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "user_list":
            kwargs["queryset"] = UserId.objects.filter(user=request.user.id)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['name', 'user_list', 'user'
                                                 ]}),

            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['name',
                                     ]}),

            ]
        return fieldsets