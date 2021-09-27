from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import ugettext as _


class LAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': "my_class floating-input"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True, 'class': "my_class floating-input"}),
    )
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

