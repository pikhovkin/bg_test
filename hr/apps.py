# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class HRConfig(AppConfig):
    name = 'hr'
    label = 'hr'
    verbose_name = _('Кадровая служба')
