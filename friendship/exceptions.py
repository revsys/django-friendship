from django.db import IntegrityError


class AlreadyExistsError(IntegrityError):
    pass


class AlreadyFriendsError(IntegrityError):
    pass


class MaxFriendsExceededError(Exception):
    """Raised when accepting a request would take a user past FRIENDSHIP_MAX_FRIENDS."""
