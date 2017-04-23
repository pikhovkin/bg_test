# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Planet(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = _('планета')
        verbose_name_plural = _('планеты')
        ordering = ['name']

    def __unicode__(self):
        return self.name
