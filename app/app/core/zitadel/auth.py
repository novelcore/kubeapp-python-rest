import time, requests
import jwt
import jwt.algorithms as algorithms
from fastapi import HTTPException, Depends, Response, Request
from fastapi.routing import APIRoute
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.status import HTTP_403_FORBIDDEN
from app.config import app_config
from app.core.zitadel.access_control import authorize_access

if app_config.auth_enabled:
    # OAuth2 scheme — only constructed when Zitadel is enabled
    oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=app_config.zitadel_auth_url,
        tokenUrl=app_config.zitadel_token_url,
    )

    def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
        '''
        Validates the bearer token against Zitadel JWK and enforces RBAC.

        Parameters:
            token (str): The token to be checked

        Returns:
            dict: The decoded token claims
        '''
        keys = app_config.jwk_data["keys"]

        jwt_options = {
            'verify_signature': True,
            'verify_exp': False,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }

        endpoint = request.scope.get("endpoint")

        for i, key in enumerate(keys):
            public_key = algorithms.RSAAlgorithm.from_jwk(key)
            try:
                decoded_token = jwt.decode(token, public_key, audience=app_config.project_id, algorithms=app_config.algorithm, verify=True, options=jwt_options)
                return authorize_access(endpoint.__name__, decoded_token)
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token has expired")
            except jwt.InvalidSignatureError:
                if i == len(keys) - 1:
                    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid signature")
            except jwt.InvalidTokenError:
                if i == len(keys) - 1:
                    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token")
                else:
                    continue

else:
    # Auth disabled — endpoints using Depends(get_current_user) are unprotected
    async def get_current_user(request: Request):
        return {}
