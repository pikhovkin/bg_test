# coding: utf-8
from __future__ import unicode_literals

from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _


USER_ROLE_CANDIDATE = 1
USER_ROLE_PADAWAN = 2
USER_ROLE_JEDI = 3

USER_ROLE_CHOICES = OrderedDict()
USER_ROLE_CHOICES[USER_ROLE_CANDIDATE] = _('Кандидат')
USER_ROLE_CHOICES[USER_ROLE_PADAWAN] = _('Падаван')
USER_ROLE_CHOICES[USER_ROLE_JEDI] = _('Джедай')
