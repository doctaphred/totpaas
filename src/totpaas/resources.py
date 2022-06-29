import time
from dataclasses import dataclass
from typing import Callable

from .totp import OTPGenerator


@dataclass
class TotpResource(OTPGenerator):
    """
    >>> from itertools import count
    >>> clock = count(28).__next__
    >>> resource = TotpResource.from_b32(clock=clock, key='lmao')

    >>> resource()
    {'time': 28, 'code': '602398'}

    >>> resource()
    {'time': 29, 'code': '602398'}

    >>> resource()
    {'time': 30, 'code': '567113'}
    """
    clock: Callable = time.time

    def __call__(self):
        time = self.clock()
        code = self.totp(time)
        return {
            'time': time,
            'code': code,
        }
