# coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _('A user with that username already exists.'),
        'duplicate_email': _('A user with that email already exists.')
    }
    username = forms.CharField(label=_('username'), max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data['username']
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'], code='duplicate_username')

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email:
            return email

        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError(self.error_messages['duplicate_email'], code='duplicate_email')
