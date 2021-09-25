import json
import os
import time

from fastapi import FastAPI, HTTPException

from .totp import OTPGenerator


class TotpResource:

    def __init__(self, params, *, clock=time.time):
        self.params = params
        self.clock = clock

    def __call__(self, name: str):
        try:
            params = self.params[name]
        except KeyError:
            raise HTTPException(status_code=404)

        totp = OTPGenerator.from_b32(**params)
        time = self.clock()
        return {
            'name': name,
            'time': time,
            'code': totp(time),
        }


params = json.loads(os.environ['TOTP_PARAMS'])
# TODO: Validate params.
app = FastAPI()
app.get("/{name}")(TotpResource(params))
