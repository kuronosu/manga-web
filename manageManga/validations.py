from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def max_genders(genders):
        print('Eje '*20)
        if genders:
            if len(genders) > 5:
                raise ValidationError(_('Invalid date - renewal in past'))
        print('Eje 2'*20)