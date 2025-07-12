import time, requests
import jwt
import jwt.algorithms as algorithms
from fastapi import HTTPException, Depends, Response, Request
from fastapi.routing import APIRoute
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.status import HTTP_403_FORBIDDEN
from app.config import app_config
from app.core.zitadel.access_control import authorize_access

# This is the OAuth2 scheme that will be used to protect the endpoints
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=app_config.zitadel_auth_url,
    tokenUrl=app_config.zitadel_token_url,
)

# This function checks the token introspection and populates the request.state variable with the user's token
def get_current_user( request: Request, token: str = Depends(oauth2_scheme)):
    '''
    This function checks the token introspection and populates the request.state variable with the user's token

    Parameters:
        token (str): The token to be checked

    Returns:
        dict: The user's token
    '''
    # # Check the token introspection endpoint to see if the token is valid
    # introspection_response = requests.post(
    #     app_config.zitadel_introspection_url,
    #     auth=(app_config.api_client_id, app_config.api_client_secret),
    #     data={'token': token}
    # )

    # if not introspection_response.json().get('active', False):
    #     raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token")
    
    # Get the keys from the JWKS endpoint
    keys = app_config.jwk_data["keys"]

    jwt_options = {
        'verify_signature': True,
        'verify_exp': False,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }

    # Get the endpoint name
    endpoint = request.scope.get("endpoint")
    
    # Iteration over the keys to find the correct one
    for i,key in enumerate(keys):
        public_key = algorithms.RSAAlgorithm.from_jwk(key)
        try:
            decoded_token = jwt.decode(token, public_key, audience=app_config.project_id, algorithms=app_config.algorithm, verify=True, options=jwt_options)
            # print(f"\n\n***** Decoded Token: {decoded_token} \n\n******")

            return authorize_access(endpoint.__name__, decoded_token)

        except jwt.ExpiredSignatureError:
            # if i == len(keys) - 1:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token has expired")
        except jwt.InvalidSignatureError:
            if i == len(keys) - 1:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid signature")
        except jwt.InvalidTokenError:
            if i == len(keys) - 1:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token")
            else:
                continue
    
    # if not decoded_token:
    #     raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid token")

