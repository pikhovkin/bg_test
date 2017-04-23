# coding: utf-8
from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse

from universe.models import Planet
from roles import USER_ROLE_CHOICES, USER_ROLE_CANDIDATE, USER_ROLE_JEDI, USER_ROLE_PADAWAN


class UserManager(BaseUserManager):
    def prepare_fields_for_create(self, fields):
        if 'email' in fields:
            email = UserManager.normalize_email(fields['email'])

            if not email and not fields['is_staff']:
                raise ValueError(_('The given email must be set'))

            fields['email'] = email

        if get_user_model().USERNAME_FIELD not in fields:
            raise ValueError(_('The `{}` field must be set').format(get_user_model().USERNAME_FIELD))

        return fields

    def create_user(self, password=None, **extra_fields):
        now = timezone.now()
        extra_fields = self.prepare_fields_for_create(extra_fields)

        user = self.model(is_staff=False, is_active=True, is_superuser=False, last_login=now, date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, **extra_fields):
        user = self.create_user(**extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.role = USER_ROLE_JEDI
        user.save(using=self._db)

        return user


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), null=True, blank=True)
    username = models.CharField(_('username'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class User(AbstractUser):
    planet = models.ForeignKey(Planet, verbose_name=_('Планета'), null=True)
    age = models.PositiveSmallIntegerField(verbose_name=_('Возраст'), null=True, blank=True)
    mentor = models.ForeignKey('self', verbose_name=_('Учитель'), null=True, blank=True, related_name='padawans')
    role = models.PositiveSmallIntegerField(verbose_name=_('Роль'), choices=USER_ROLE_CHOICES.iteritems(),
                                            default=USER_ROLE_CANDIDATE)

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['id']

    def get_absolute_url(self):
        if self.role == USER_ROLE_JEDI:
            return reverse('view_jedi_candidates', args=(self.id,))
        elif self.role == USER_ROLE_PADAWAN:
            return reverse('view_padawan', args=(self.id,))
        elif self.role == USER_ROLE_CANDIDATE:
            return reverse('get_test', args=(self.id,))

        return ''
