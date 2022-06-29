import json
import os

from fastapi import FastAPI, Response

from .resources import TotpResource


def from_environ(environ=os.environ):
    return from_params(json.loads(environ['TOTP_PARAMS']))


def from_params(params):
    app = FastAPI()

    # Add a basic health check endpoint.
    app.add_api_route('/ok', lambda: Response('ok'))

    # Add the TOTP endpoints.
    for name, kwargs in params.items():
        endpoint = TotpResource.from_b32(**kwargs)
        app.add_api_route(f'/totp/{name}', endpoint)

    return app
