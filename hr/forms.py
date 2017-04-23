# coding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model

from models import Question, Answer


User = get_user_model()


class CandidateForm(forms.ModelForm):
    username = forms.CharField(label=_('Имя кандидата'))
    email = forms.CharField(required=True)
    age = forms.IntegerField(label=_('Возраст'), required=True, min_value=0)

    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'planet')


class QuestionForm(forms.ModelForm):
    answer = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Question
        fields = ('text',)

        widgets = {
            'text': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(label_suffix='', *args, **kwargs)

        if 'value' not in self.fields['answer'].widget.attrs:
            self.fields['answer'].widget.attrs['value'] = 'off'

        self.fields['answer'].label = self.initial.get('text', '')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('question', 'answer')
