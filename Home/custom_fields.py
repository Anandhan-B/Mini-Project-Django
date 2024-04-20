from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class TenDigitBigIntegerField(models.BigIntegerField):
    def __init__(self, *args, **kwargs):
        kwargs['validators'] = [self.validate_ten_digits]
        super().__init__(*args, **kwargs)

    def validate_ten_digits(self, value):
        if value < 10**9 or value >= 10**10:
            raise ValidationError(
                _('%(value)s is not a 10-digit number.'),
                params={'value': value},
            )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Remove the default validator, since we're adding a custom one
        kwargs.pop('validators', None)
        return name, path, args, kwargs
