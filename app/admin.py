from django.contrib import admin
from .models import InstagramUser, Limit, Template, SystemSetting, UserId, ListName, SendMessageByList, \
    SendMessageByUrl, MessageTemplate, NameMessageTemplate
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User, Group, Permission
from django.db import IntegrityError
from django import forms
from .forms import UserIdForm
from django.contrib.contenttypes.models import ContentType


models = {
    'InstagramUser':                {'view': True, 'add': True, 'change': True, 'delete': True},
    'NameMessageTemplate':          {'view': True, 'add': True, 'change': True, 'delete': False},
    'UserId':                       {'view': True, 'add': True, 'change': True, 'delete': True},
    'ListName':                     {'view': True, 'add': True, 'change': True, 'delete': True},
    'SendMessageByList':            {'view': True, 'add': True, 'change': True, 'delete': True},
    'SendMessageByUrl':             {'view': True, 'add': True, 'change': True, 'delete': True},
    'MessageTemplate':              {'view': True, 'add': True, 'change': True, 'delete': True},
    'Template':                     {'view': True, 'add': False, 'change': True, 'delete': False},

}


def add_permissions_to_group(group_name, permissions):
    group, created = Group.objects.get_or_create(name=group_name)

    for model, permissions in permissions.items():
        content_type = ContentType.objects.get(app_label='app', model=model.lower())
        for permission_type, allowed in permissions.items():
            codename = f'{permission_type}_{model.lower()}'
            try:
                permission = Permission.objects.get(codename=codename, content_type=content_type)
            except Permission.DoesNotExist:
                permission = Permission.objects.create(codename=codename, name=f'Can {permission_type} {model}',
                                                       content_type=content_type)

            if allowed:
                group.permissions.add(permission)


add_permissions_to_group('Partner', models)


@admin.register(InstagramUser)
class InstagramUserAdmin(admin.ModelAdmin):
    list_display = ['login', 'age', ]
    search_fields = ['login', ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['login', 'age', 'system', 'country',
                    'country_code', 'locale', 'timezone',
                    ]

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['login', 'password', 'age', 'system',
                                     'country', 'country_code', 'locale',
                                     'user', 'timezone',
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['login', 'password', 'age', 'system',
                                     'country', 'country_code', 'locale',
                                     'timezone',
                                     ]
                          }
                 ),
            ]

        return fieldsets


@admin.register(Limit)
class LimitAdmin(admin.ModelAdmin):
    list_display = ['name', 'limit', 'description']

    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_add_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.user:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['key', 'value', 'user',
                                     'description', 'account'
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['value',
                                     ]
                          }
                 ),
            ]

        return fieldsets

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['id', 'account', 'key',
                    'value', 'description',
                    ]


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['url', 'page_id']

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['url', 'page_id', 'user',
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['url',
                                     ]
                          }
                 ),
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

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
                ('Дані', {'fields': ['name', 'user_list', 'user',
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['name', 'user_list'
                                     ]
                          }
                 ),
            ]

        return fieldsets

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['name', 'user_list', ]


@admin.register(SendMessageByUrl)
class SendMessageByUrlAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "accounts":
            kwargs["queryset"] = InstagramUser.objects.filter(user=request.user.id)

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['url', 'direct_message',
                    'user', 'accounts', ]

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['url', 'direct_message', 'user',
                                     'accounts', 'created_at',
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['url', 'direct_message',
                                     'accounts',
                                     ]
                          }
                 ),
            ]

        return fieldsets

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'direct_message':
            kwargs['queryset'] = MessageTemplate.objects.filter(user=request.user.id).only('value')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(SendMessageByList)
class SendMessageByListAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['lists', 'direct_message',
                    'accounts', 'created_at',
                    ]

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['url', 'direct_message', 'user',
                                     'accounts',
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['lists', 'direct_message',
                                     'accounts',
                                     ]
                          }
                 ),
            ]

        return fieldsets

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "lists":
            kwargs["queryset"] = ListName.objects.filter(user=request.user.id)
        if db_field.name == "accounts":
            kwargs["queryset"] = InstagramUser.objects.filter(user=request.user.id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'direct_message':
            kwargs['queryset'] = MessageTemplate.objects.filter(user=request.user.id).only('value')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'key':
            kwargs['queryset'] = NameMessageTemplate.objects.filter(user=request.user.id).only('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['key', 'value', 'user',
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['key', 'value',
                                     ]
                          }
                 ),
            ]

        return fieldsets

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['key', 'value',
                    ]


@admin.register(NameMessageTemplate)
class NameMessageTemplateAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.user:
            obj.user = User.objects.get(pk=request.user.id)
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            fieldsets = [
                ('Дані', {'fields': ['name', 'user',
                                     ]
                          }
                 ),
            ]
        else:
            fieldsets = [
                ('Дані', {'fields': ['name',
                                     ]
                          }
                 ),
            ]

        return fieldsets

    def get_list_display(self, request):
        if request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            return ['name',
                    ]