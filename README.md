# Implementation of an OIDC github client

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

1. verify that the token is authentic 






