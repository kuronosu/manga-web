import re
from django.contrib.auth import validators
from django.utils.translation import gettext_lazy as _

class UnicodeUsernameValidator(validators.UnicodeUsernameValidator):
    regex = r'^[\w.+-]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and ./+/-/_ characters.'
    )