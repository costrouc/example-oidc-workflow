# Implementation of an OIDC github client

Here we implement OIDC authentication for github-actions entirely
within the github-action.

 - client `oidc-exchange.py` (github-action)
 - server `main.py` ("provider" for example vault, cloud providers, pypi)

## High Level

The workflow goes as follows. Call an audience route on your web
server which returns the given audience field that should be set for
the OIDC token. It does not have to be this exact route.

```yaml
GET https://<domain>/_/oidc/audience

{
   audience: <custom-audience-name>
}
```

From the `audience` field then request from github actions a token
which has the given audience.

```python
import id

try:
    oidc_token = id.detect_credential(audience=oidc_audience)
except id.IdentityError as identity_error:
    # communicate error calling github-actions OIDC to mint token
```

Call a post method on your web server to return a given api token.

```python
POST https://{repository_domain}/_/oidc/github/token

{
    "token": "..."
}
```

Before returning `token` as a response the web server should validate
the token.

1. download the public keys from github for validating jwts
2. verify that the jwt token is authentic (check iss, sub, aud, exp, nbf, jti, etc.)
3. next validate additional claims from the jwt e.g. repository, branch, workflow, etc.
4. return a properly scoped token

Done!

# License

MIT



