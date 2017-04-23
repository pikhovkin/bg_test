# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Test, Question


class TestAdmin(admin.ModelAdmin):
    list_display = ('code',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test')
    list_display_links = ('text',)


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
