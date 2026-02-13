from typing import Annotated

from fastapi.responses import RedirectResponse
import starsessions
from fastapi import Depends, FastAPI, status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starsessions import SessionAutoloadMiddleware, SessionMiddleware
from contextlib import asynccontextmanager
from starlette.responses import Response
from starsessions.stores.redis import RedisStore

from app.internal.settings import DatabaseSettings
from app.models.oidc_model import OIDCToken
from app.utils.exception.common_exceptions import RequiresLogin, RequiresDatas
from app.database.database import create_db_and_tables, get_db
from app.internal import AppRoutesSettings
from app.routers import home, m2m
from app.routers import auth
from app.session import OidcSession
from sqlalchemy.pool import AsyncAdaptedQueuePool
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "https://producer.smartland.lan",
    "https://auth.smartland.lan",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



store = RedisStore(url='redis://redis:6379', prefix='smartland_session_')


app.add_middleware(SessionAutoloadMiddleware)
app.add_middleware(SessionMiddleware, store=store, cookie_https_only=False, cookie_path='/')

app.add_middleware(SQLAlchemyMiddleware, db_url=
                   f"postgresql+asyncpg://{DatabaseSettings.sqlalchemy_database_server_user}:"
                   f"{DatabaseSettings.sqlalchemy_database_server_password}@"
                   f"{DatabaseSettings.sqlalchemy_database_server_name}:"
                   f"{DatabaseSettings.sqlalchemy_database_server_port}/"
                   f"{DatabaseSettings.sqlalchemy_database_server_database}", 
                   engine_args={
                       "echo": True,
                       "poolclass": AsyncAdaptedQueuePool
                   })



app.include_router(auth.router)
app.include_router(home.router)
app.include_router(m2m.router)

@app.exception_handler(RequiresLogin)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(url=AppRoutesSettings.error_page_frontend)

@app.exception_handler(RequiresDatas)
async def requires_datas(request: Request, _: Exception):
    return RedirectResponse(url=AppRoutesSettings.error_page_frontend)

@app.get('/')
async def homepage(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]):
    return Response(status_code=status.HTTP_200_OK)


