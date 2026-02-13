from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4
from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from app.cruds import user_crud, user_login_crud
from app.schemas.user_login_schema import IUserLoginCreate
from app.session import OidcSession
from app.utils.exception.common_exceptions import RequiresLogin
from app.internal import  AppRoutesSettings
from app.utils.jwt_token import create_token
from dateutil.parser import isoparse
import datetime

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.get("/login", tags=["auth"])
async def login(request: Request):

    user_name = request.headers.get('x-webauth-consumer')

    if not user_name:
        raise RequiresLogin(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token.")

    ## To be compatible with later implementation of OpenID-Connect it create a jwt-token
    expire_in = 600
    iat_time = int(isoparse(datetime.datetime.now(datetime.timezone.utc).isoformat()).timestamp()) 
    id_token = create_token(sub=user_name, iat=iat_time, exp_in=expire_in)
    access_token = {
        'access_token': id_token,
        'id_token': id_token,
        'token_type': 'Bearer',
        'expires_in': expire_in,
        'expires_at': iat_time + expire_in
    }
    request.session['access_token'] = access_token

    session_id = str(uuid4())
    if not request.session.get('login_session'):
        request.session['login_session'] = session_id
        try:
            oidc = OidcSession()
            oidc_token = await oidc(request=request,oidc_token=OidcSession.get_oidc_token(request=request))
            
            db_user = await user_crud.create(obj_in=oidc_token.user_info)
            

            await user_login_crud.create(
                obj_in=IUserLoginCreate(
                    user_id=db_user.id,
                    login_oidc=datetime.datetime.fromtimestamp(oidc_token.user_info.auth_time, tz=timezone.utc),
                    id=session_id
                )
            )
        except OAuthError as ex:
            print(ex)
            raise RequiresLogin(status_code=status.HTTP_403_FORBIDDEN, detail="Could not fetch access token.")
        
    return RedirectResponse(url=AppRoutesSettings.landing_page)

    


@router.get("/logout", tags=["auth"])
async def logout(request: Request, response: Response):
    request.session.clear()
    return RedirectResponse(url=AppRoutesSettings.login_page_frontend)
