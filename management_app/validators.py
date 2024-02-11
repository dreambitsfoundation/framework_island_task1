from django.core.exceptions import ValidationError


def validate_phone_number(value):
    value = str(value)
    if not value.isnumeric() or len(value) != 10:
        raise ValidationError(
            ("%(value)s is not an valid phone number"),
            params={"value": value},
        )
