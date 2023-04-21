from fastapi import FastAPI
import pydantic
import jwt


class AudienceResponse(pydantic.BaseModel):
    audience: str


class TokenRequest(pydantic.BaseModel):
    token: str


class TokenResponse(pydantic.BaseModel):
    token: str


app = FastAPI()


@app.get("/_/oidc/audience")
async def get_audience() -> AudienceResponse:
    return AudienceResponse(audience="example-oidc-workflow")


@app.post("/_/oidc/github/token")
async def create_token(token: TokenRequest):
    payload = jwt.decode(token.token)
    print(payload)
    return TokenResponse(token="asdf")
