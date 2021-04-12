from datetime import date, datetime

import pendulum
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import DateTimeField, Field
from pendulum.parsing import ParserError

from .form import PendulumField as PendulumFormField

__all__ = ["PendulumField"]


class PendulumField(DateTimeField):
    """
    A date and time, including timezone information, represented in Python by a `pendulum.DateTime` object
    """

    def get_prep_value(self, value):
        value = Field.get_prep_value(self, value)
        value = self.to_python(value)
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None

        return pendulum.instance(value, tz=settings.TIME_ZONE)

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = pendulum.now(tz=settings.TIME_ZONE)
            setattr(model_instance, self.attname, value)
            return value

        return Field.pre_save(self, model_instance, add)

    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, pendulum.DateTime):
            value = value.in_tz(settings.TIME_ZONE)
            return value

        if isinstance(value, datetime):
            value = pendulum.instance(value, tz=settings.TIME_ZONE)
            return value

        if isinstance(value, date):
            value = pendulum.datetime(value.year, value.month, value.day, tz=settings.TIME_ZONE)
            return value

        try:
            return pendulum.parse(value).in_tz(settings.TIME_ZONE)
        except ParserError:
            error_code = "invalid_datetime"
            raise ValidationError(
                self.error_messages[error_code],
                code=error_code,
                params={"value": value},
            )

    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if isinstance(val, pendulum.DateTime):
            return val.to_iso8601_string()

        return super().value_to_string(obj)

    def formfield(self, **kwargs):
        defaults = {"form_class": PendulumFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
