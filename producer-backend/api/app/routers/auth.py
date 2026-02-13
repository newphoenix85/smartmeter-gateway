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
from app.internal.oauth import oauth_client
from app.internal import OAuth2Settings, AppRoutesSettings

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.get("/login", tags=["auth"])
async def login(request: Request):
    authorization_url, state = oauth_client.create_authorization_url(
            OAuth2Settings.authorize_url)
    return RedirectResponse(authorization_url)
    


@router.get("/logout", tags=["auth"])
async def logout(request: Request):
    await OidcSession.revoke_access_token(request)
    await OidcSession.revoke_refresh_token(request)
    request.session.clear()
    return RedirectResponse(url=AppRoutesSettings.login_page_frontend)





@router.get("/oauth2", tags=["auth"])
async def auth(request: Request):
    try:
        code = request.query_params.get('code')
        access_token = await oauth_client.fetch_token(OAuth2Settings.token_url, code=code)
        request.session['access_token'] = access_token

        session_id = str(uuid4())
        request.session['login_session'] = session_id

        oidc = OidcSession()
        oidc_token = await oidc(request=request,oidc_token=OidcSession.get_oidc_token(request=request))
        
        db_user = await user_crud.create(obj_in=oidc_token.user_info)

        await user_login_crud.create(
            obj_in=IUserLoginCreate(
                user_id=db_user.id,
                login_oidc=datetime.fromtimestamp(oidc_token.user_info.auth_time, tz=timezone.utc),
                id=session_id
            )
        )
        return RedirectResponse(url=AppRoutesSettings.landing_page)

    except OAuthError as ex:
        print(ex)
        raise RequiresLogin(status_code=status.HTTP_403_FORBIDDEN, detail="Could not fetch access token.")
