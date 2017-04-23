# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Test(models.Model):
    code = models.CharField(verbose_name=_('Код теста'), max_length=30, unique=True)
    created = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=timezone.now)

    class Meta:
        verbose_name = _('тестовое испытание')
        verbose_name_plural = _('тестовые испытания')
        ordering = ['created']

    def __unicode__(self):
        return self.code


class Question(models.Model):
    test = models.ForeignKey(Test, verbose_name=_('Тестовое испытание'), related_name='questions')
    text = models.CharField(verbose_name=_('Текст'), max_length=255)

    class Meta:
        verbose_name = _('вопрос')
        verbose_name_plural = _('вопросы')
        ordering = ['test', 'id']
        unique_together = (('test', 'text'),)

    def __unicode__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Кандидат'), related_name='answers')
    question = models.ForeignKey(Question, verbose_name=_('Вопрос'), related_name='answers')
    answer = models.BooleanField(verbose_name=_('Ответ'), default=False)

    class Meta:
        verbose_name = _('ответ кандидата')
        verbose_name_plural = _('ответы кандидатов')
        ordering = ['user', 'question']
