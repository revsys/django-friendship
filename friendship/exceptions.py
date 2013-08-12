from django.core.exceptions import ValidationError


class AlreadyExistsError(ValidationError):
    pass
