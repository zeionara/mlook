from functools import wraps


def as_tuple(function):

    @wraps(function)
    def _as_tuple(*args, **kwargs):
        return tuple(
            function(*args, **kwargs)
        )

    return _as_tuple
