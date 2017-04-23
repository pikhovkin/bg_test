# coding: utf-8

from django.contrib import admin

from models import Planet


class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Planet, PlanetAdmin)
