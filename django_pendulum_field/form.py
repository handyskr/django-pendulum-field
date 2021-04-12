from datetime import date, datetime

import pendulum
from django.core.exceptions import ValidationError
from django.forms import DateTimeField
from django.utils import timezone
from pendulum.parsing import ParserError

__all__ = ["PendulumField"]


class PendulumField(DateTimeField):
    def prepare_value(self, value):
        return value.to_datetime_string()

    def to_python(self, value):
        current_timezone = timezone.get_current_timezone()

        if value is None:
            return value
        if isinstance(value, pendulum.DateTime):
            return value
        if isinstance(value, datetime):
            value = pendulum.instance(value, tz=current_timezone)
            return value
        if isinstance(value, date):
            value = pendulum.datetime(value.year, value.month, value.day, tz=current_timezone)
            return value

        try:
            return pendulum.parse(value, tz=current_timezone)
        except ParserError:
            error_code = "invalid_datetime"
            raise ValidationError(
                self.error_messages[error_code],
                code=error_code,
                params={"value": value},
            )

    def strptime(self, value, format):
        return pendulum.from_format(value, format, timezone.get_current_timezone())
