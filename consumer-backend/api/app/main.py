from typing import Annotated

from fastapi.responses import RedirectResponse
import starsessions
import asyncio
from app.core.simulator import simulate_smart_meter_readings
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
from app.internal import AppRoutesSettings, RedisSessionManagerSettings, DatabaseSettings
from app.routers import home
from app.routers import auth
from app.session import OidcSession
from sqlalchemy.pool import AsyncAdaptedQueuePool
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("uvicorn")
    logger.info("Lifespan: Starting up...")
    
    await create_db_and_tables()
    logger.info("Lifespan: DB tables created.")

    asyncio.create_task(simulate_smart_meter_readings())
    logger.info("Lifespan: Simulator task created.")
    
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "https://consumer.tenant.lan",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



store = RedisStore(url=f'redis://{RedisSessionManagerSettings.host}:{RedisSessionManagerSettings.port}', prefix='smartland_session_')


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

@app.exception_handler(RequiresLogin)
async def requires_login(request: Request, _: Exception):
    return RedirectResponse(url=AppRoutesSettings.error_page_frontend)

@app.exception_handler(RequiresDatas)
async def requires_datas(request: Request, _: Exception):
    return RedirectResponse(url=AppRoutesSettings.error_page_frontend)

@app.get('/')
async def homepage(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]):
    return Response(status_code=status.HTTP_200_OK)


