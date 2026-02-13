
import base64
import datetime
import json
from typing import Annotated

from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from fastapi import Depends, HTTPException, status

from pydantic import ValidationError
from starlette.requests import Request, HTTPConnection
from starlette.responses import Response

from app.models import OIDCToken, UserOidc
from app.utils.exception.common_exceptions import RequiresLogin



class OidcSession:

    @staticmethod
    def parse_id_token(token: str) -> dict:
        parts = token.split(".")
        if len(parts) != 3:
            raise Exception("Incorrect id token format")
        payload = parts[1]
        padded = payload + '=' * (4 - len(payload) % 4)
        decoded = base64.b64decode(padded)
        return json.loads(decoded)

    @staticmethod
    def get_oidc_token(request: HTTPConnection) -> OIDCToken:
        access_token = request.session.get('access_token')
        print('access_token: ', access_token)
        if not access_token:
            raise RequiresLogin(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")
        try:
            user_info = UserOidc.model_validate(OidcSession.parse_id_token(access_token.get('id_token')))
            access_token['user_info'] = user_info.model_dump()
            return OIDCToken.model_validate(access_token)
        except ValidationError as ex:
            print(f"Invalid authentik user data -- error: {ex}")
            raise RequiresLogin(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme.")
        

    async def __call__(
            self,
            request: HTTPConnection, 
            oidc_token: Annotated[OIDCToken, Depends(get_oidc_token)]) -> OIDCToken:

        expires_at = oidc_token.expires_at
        now = int(datetime.datetime.timestamp(datetime.datetime.now()))
        print(f"oidc authentication time for user "
                     f"{oidc_token.user_info.preferred_username}:{oidc_token.user_info.id}: "
                     f"{oidc_token.user_info.auth_time}")
        if expires_at < now:
            
            print(f"session expired for user "
                f"{oidc_token.user_info.preferred_username}:{oidc_token.user_info.id}")
            oidc_token = OidcSession.get_oidc_token(request)
            print(f"valid refresh token fetched for user "
                            f"{oidc_token.user_info.preferred_username}:{oidc_token.user_info.id}")
        return oidc_token


    

    

    

