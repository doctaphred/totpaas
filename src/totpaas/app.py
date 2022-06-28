import json
import os

from fastapi import FastAPI, Response

from .resources import TotpResource


def from_environ(environ=os.environ):
    return from_params(json.loads(environ['TOTP_PARAMS']))


def from_params(params):
    app = FastAPI()
    # Add a basic health check endpoint.
    app.add_api_route('/ok', lambda: 'ok', response_class=Response)
    # Add the TOTP endpoint.
    app.add_api_route('/totp/{name}', TotpResource.from_b32_params(params))
    return app
