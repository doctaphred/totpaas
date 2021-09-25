import json
import os
import time

from fastapi import FastAPI, HTTPException

from .totp import OTPGenerator


class TotpResource:

    def __init__(self, generators, *, clock=time.time):
        self.generators = generators
        self.clock = clock

    @classmethod
    def from_params(cls, params, **kwargs):
        generators = {
            name: OTPGenerator.from_b32(**kwargs)
            for name, kwargs in params.items()
        }
        return cls(generators, **kwargs)

    def __call__(self, name: str):
        try:
            totp = self.generators[name]
        except KeyError:
            raise HTTPException(status_code=404)

        time = self.clock()
        return {
            'name': name,
            'time': time,
            'code': totp(time),
        }


params = json.loads(os.environ['TOTP_PARAMS'])
resource = TotpResource.from_params(params)

app = FastAPI()
app.get("/{name}")(resource)
