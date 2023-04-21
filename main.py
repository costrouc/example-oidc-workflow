import json
import datetime

from fastapi import FastAPI
import pydantic
import requests
import jwt


class AudienceResponse(pydantic.BaseModel):
    audience: str


class TokenRequest(pydantic.BaseModel):
    token: bytes


class TokenResponse(pydantic.BaseModel):
    token: str


def get_public_keys():
    base_url = 'https://token.actions.githubusercontent.com/'
    jwks_url = requests.get(f'{base_url}.well-known/openid-configuration').json()['jwks_uri']

    public_keys = {}
    data = requests.get(jwks_url).json()
    for jwk in data['keys']:
        public_keys[jwk['kid']] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    return public_keys

TRUSTED_PUBLIC_KEYS = get_public_keys()


app = FastAPI()


@app.get("/_/oidc/audience")
async def get_audience() -> AudienceResponse:
    return AudienceResponse(audience="example-oidc-workflow")


@app.post("/_/oidc/github/mint-token")
async def create_token(token: TokenRequest):
    header = jwt.get_unverified_header(token.token)
    print(header)
    public_key = TRUSTED_PUBLIC_KEYS[header['kid']]
    payload = jwt.decode(token.token, public_key, audience="example-oidc-workflow", algorithms=['RS256'])
    print(payload)
    print(datetime.datetime.fromtimestamp(payload['iat']))
    print(datetime.datetime.utcnow())
    print(datetime.datetime.now())
    return TokenResponse(token="asdf")
