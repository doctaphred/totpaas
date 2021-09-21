import json
import os
import time

from fastapi import FastAPI, HTTPException
from mintotp import hotp  # type: ignore


def totp(time, *, key, time_step, digits, digest):
    counter = int(time / time_step)
    return hotp(key, counter, digits, digest)


class TotpResource:

    def __init__(self, params, *, clock=time.time):
        self.params = params
        self.clock = clock

    def __call__(self, name: str):
        try:
            params = self.params[name]
        except KeyError:
            raise HTTPException(status_code=404)

        time = self.clock()
        return {
            'name': name,
            'time': time,
            'value': totp(time=time, **params),
        }


params = json.loads(os.environ['TOTP_PARAMS'])
# TODO: Validate params.
app = FastAPI()
app.get("/{name}")(TotpResource(params))
