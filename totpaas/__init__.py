__version__ = '0.1.0'
import json
import os

from fastapi import FastAPI

from .main import TotpResource


params = json.loads(os.environ['TOTP_PARAMS'])
resource = TotpResource.from_b32_params(params)

app = FastAPI()
app.add_api_route("/{name}", resource)
