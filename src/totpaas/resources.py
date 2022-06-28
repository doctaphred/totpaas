import time

from fastapi import HTTPException

from .totp import OTPGenerator


class TotpResource:
    """
    >>> from itertools import count
    >>> clock = count(28).__next__
    >>> params = {'ayy': {'key': 'lmao'}}
    >>> resource = TotpResource.from_b32_params(params, clock=clock)

    >>> resource('ayy')
    {'name': 'ayy', 'time': 28, 'code': '602398'}

    >>> resource('lmao')
    Traceback (most recent call last):
      ...
    fastapi.exceptions.HTTPException: 404

    >>> resource('ayy')
    {'name': 'ayy', 'time': 29, 'code': '602398'}

    >>> resource('ayy')
    {'name': 'ayy', 'time': 30, 'code': '567113'}
    """

    def __init__(self, generators, *, clock=time.time):
        self.generators = generators
        self.clock = clock

    @classmethod
    def from_b32_params(cls, params, **kwargs):
        generators = {
            name: OTPGenerator.from_b32(**kwargs)
            for name, kwargs in params.items()
        }
        return cls(generators, **kwargs)

    def __call__(self, name: str):
        try:
            totp = self.generators[name]
        except KeyError as exc:
            raise HTTPException(404) from exc

        time = self.clock()
        return {
            'name': name,
            'time': time,
            'code': totp(time),
        }
