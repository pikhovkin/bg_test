# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from forms import UserCreationForm


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'planet', 'role', 'age',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional'), {'fields': ('mentor',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username')}
        ),
    )
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_superuser', 'date_joined',
                    'planet', 'age', 'mentor', 'role')
    list_display_links = ('email', 'username')
    ordering = ('username',)


admin.site.register(User, UserAdmin)
