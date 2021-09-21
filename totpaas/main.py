import json
import os
import time

from fastapi import FastAPI, HTTPException
from mintotp import hotp  # type: ignore


def totp(key, time, *, time_step, digits, digest):
    counter = int(time / time_step)
    return hotp(key, counter, digits, digest)


class TotpResource:

    def __init__(self, keys, *, clock=time.time):
        self.keys = keys
        self.clock = clock

    def params(self):
        return dict(
            digits=6,
            time_step=30,
            digest='sha1',
            time=self.clock(),
        )

    def __call__(self, name: str):
        try:
            key = self.keys[name]
        except KeyError:
            raise HTTPException(status_code=404)

        # TODO: URL params?
        params = self.params()
        value = totp(key, **params)
        return {
            'name': name,
            **params,
            'value': value,
        }


keys = json.loads(os.environ['TOTP_KEYS'])
app = FastAPI()
app.get("/{name}")(TotpResource(keys))
