from datetime import datetime, timezone
from typing import Annotated, List
import json
from fastapi import APIRouter, Depends, status
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from app.models.smartland_smgw_model import SmartlandSMGW
from app.schemas.smartland_smgw_schema import ISmartlandSMGWCreate
from app.cruds import user_crud, smartland_consumer_crud
from app.models import OIDCToken
from app.session import OidcSession
from app.internal import AppRoutesSettings
from app.utils.exception.common_exceptions import RequiresDatas
from uuid import uuid4


router = APIRouter(
    prefix="/api/home",
    tags=["home"]
)


@router.get("/", tags=["home"])
async def landing(request: Request, 
                  oidc_token: Annotated[OIDCToken, Depends(OidcSession())]):
    return RedirectResponse(url=AppRoutesSettings.home_url)

@router.get("/get", tags=["home"])
async def getReadingValues(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]) -> JSONResponse: # type: ignore
    print('I am in home/get')
    # SECURITY PRINCIPLE: Identification & Authentication
    # The user is identified via OIDC Token (oidc_token) which is verified by the OidcSession dependency.
    
    db_user = await user_crud.create(obj_in=oidc_token.user_info)
    print(db_user)
    
    # SECURITY PRINCIPLE: Authorization
    # Producer backend shows all data to authenticated users (Operator View)
    # This is the WAN interface where the energy provider views all customer data
    
    print(f"User {db_user.id} authenticated. Fetching all data for operator view.")
    reading_datas = await smartland_consumer_crud.read_all()

    print(reading_datas)
    # Convert SQLModel objects to dictionaries with JSON-compatible types (datetime -> str)
    json_dump = json.dumps([row.model_dump(mode='json') for row in reading_datas])
    print(json_dump)
    return JSONResponse(json_dump, status_code=status.HTTP_200_OK)

@router.post("/add", tags=["home"])
async def addReadingValue(request: Request,  oidc_token: Annotated[OIDCToken, Depends(OidcSession())]) -> JSONResponse:
    print('I am in addReadingValue')
    print(oidc_token.user_info)
    try:
        reading_id = str(uuid4())
        body = await request.json()
        reading_meter_number = int(body['reading_meter_number'])
        meter_number = int(body["meter_number"])
        readingDate = datetime.fromisoformat(body['readingDate'])
        db_user = await user_crud.create(obj_in=oidc_token.user_info)
        db_response = await smartland_consumer_crud.create(
            obj_in=ISmartlandSMGWCreate(
                id=reading_id,
                user_id=db_user.id,
                reading_date=readingDate,
                reading_meter_number=reading_meter_number,
                meter_number=meter_number
            )
        )
        json_dump = json.dumps(db_response.model_dump_json())
    
        return JSONResponse(json_dump, status_code=status.HTTP_200_OK)
    except Exception as ex:
        print(ex)
        return JSONResponse([], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    