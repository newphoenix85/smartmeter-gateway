from .settings import OAuth2Settings
from authlib.integrations.httpx_client import AsyncOAuth2Client

oauth_client = AsyncOAuth2Client(
    client_id=OAuth2Settings.client_id,
    client_secret=OAuth2Settings.client_secret,
    scope=OAuth2Settings.scope,
    redirect_uri=OAuth2Settings.redirect_uri,
    grant_type=OAuth2Settings.grant_type,
    auth_url=OAuth2Settings.authorize_url,
    verify = OAuth2Settings.verify,
    authorization_response=OAuth2Settings.authorization_response
)





