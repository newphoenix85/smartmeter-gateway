from datetime import datetime, timezone
from http.client import HTTPException
from typing import Annotated, List
import json
import httpx
import uuid
import base64
from fastapi import APIRouter, Depends, status
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
import traceback
from app.models.smartland_smgw_model import SmartlandSMGW
from app.models.logbook_model import SmartlandLogbook, TypeEnum, LevelEnum
from app.schemas.smartland_smgw_schema import ISmartlandSMGWCreate
from app.schemas.smartland_logbook_schema import ILogbookCreate
from app.cruds import user_crud, smartland_smgw_crud, smartland_logbook_crud
from app.models import OIDCToken
from app.session import OidcSession
from app.internal import AppRoutesSettings, ProducerSettings
from app.utils.exception.common_exceptions import RequiresDatas
from uuid import uuid4

router = APIRouter(
    prefix="/api/home",
    tags=["home"]
)


@router.get("/", tags=["home"])
async def landing(request: Request, 
                  # SECURITY PRINCIPLE: Identification & Authentication
                  # User identity is verified via OIDC Token before access is granted.
                  oidc_token: Annotated[OIDCToken, Depends(OidcSession())]):
    return RedirectResponse(url=AppRoutesSettings.home_url)

@router.get("/me", tags=["home"])
async def get_user_info(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]):
    """
    Endpoint to retrieve the current logged-in user's information.
    """
    return JSONResponse(content=oidc_token.user_info.model_dump(), status_code=status.HTTP_200_OK)

@router.get("/get", tags=["home"])
async def getReadingValues(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]) -> JSONResponse: 
    """
    Endpoint to retrieve reading values for a user based on their OIDC token.

    Args:
        request (Request): The incoming HTTP request.
        oidc_token (OIDCToken): The OIDC token containing user information, 
                                obtained through dependency injection.

    Returns:
        JSONResponse: A JSON response containing a list of reading values or an empty list,
                      with an appropriate HTTP status code.
    """
    try:
        # Create or get a user in the database using the information from the OIDC token.
        db_user = await user_crud.create(obj_in=oidc_token.user_info)
        # Retrieve all reading data associated with the created user.
        reading_datas = await smartland_smgw_crud.read(obj_in=db_user.id)
        # Serialize the reading data to JSON format.
        json_dump = json.dumps([row.model_dump_json() for row in reading_datas])
        # Return the JSON response with a 200 OK status.
        return JSONResponse(json_dump, status_code=status.HTTP_200_OK)
    except Exception as ex:
        # Print the exception for debugging purposes.
        print(ex)
        # Return an empty JSON response with a 500 Internal Server Error status.
        return JSONResponse([], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/getLast", tags=["home"])
async def getLastValue(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]) -> JSONResponse: 
    """
    Endpoint to retrieve the last added data for a user based on their OIDC token.

    Args:
        request (Request): The incoming HTTP request.
        oidc_token (OIDCToken): The OIDC token containing user information, 
                                obtained through dependency injection.

    Returns:
        JSONResponse: A JSON response containing the last added data or an empty object,
                      with an appropriate HTTP status code.
    """
    try:
        # Create or get a user in the database using the information from the OIDC token.
        db_user = await user_crud.create(obj_in=oidc_token.user_info)
        # Retrieve the last added data for the user.
        reading_datas = await smartland_smgw_crud.readOne(obj_in=db_user.id)
        # Check if any added data was found.
        if(reading_datas):
            # If data is found, serialize it to JSON format.
            json_dump = json.dumps(reading_datas.model_dump_json())
        else:
            # If no data is found, return an empty JSON object.
            json_dump = json.dumps({})
        # Return the JSON response with a 200 OK status.
        return JSONResponse(json_dump, status_code=status.HTTP_200_OK)
    except Exception as ex:
        # Print the exception for debugging purposes.
        print(ex)
        # Return an empty JSON response with a 500 Internal Server Error status.
        return JSONResponse({}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.post("/new", tags=["home"])
async def getNewDatasFromSensor(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]): 
    """
    HONEYPOT ENDPOINT: 
    Manual data entry is no longer allowed. 
    Any attempt to use this endpoint is considered a security violation.
    """
    import logging
    
    # Get user info for logging
    user_id = oidc_token.user_info.sub if oidc_token.user_info else "Unknown"
    client_ip = request.client.host if request.client else "Unknown"
    
    # Log the security event
    logging.warning(f"SECURITY EVENT: Unauthorized manual data entry attempt detected.")
    logging.warning(f"User: {user_id}")
    logging.warning(f"Source IP: {client_ip}")
    logging.warning(f"Action: Blocked request to /api/home/new")

    logbookCreate: ILogbookCreate = ILogbookCreate(
            id=uuid.uuid4(),
            user_id=user_id,
            type=TypeEnum.SYS,
            event= f"SECURITY EVENT: Unauthorized manual data entry attempt detected. Source IP: {client_ip}. Action: Blocked request to /api/home/new",
            level=LevelEnum.F,
            checked=False
    )

    await smartland_logbook_crud.create(
        obj_in=logbookCreate
    )

    # Return 403 Forbidden
    return JSONResponse(
        content={"detail": "Manual data entry is disabled for security reasons. This event has been logged."}, 
        status_code=status.HTTP_403_FORBIDDEN
    )


@router.get("/test", tags=["home"])
async def testProducer(request: Request, oidc_token: Annotated[OIDCToken, Depends(OidcSession())]) -> JSONResponse: 

    # HTTP-Anfrage an den Producer-Server senden
    producer_url = "https://producer.smartland.lan/api/home/add"
    headers = {
        "Authorization": f"Basic {ProducerSettings.smartland_username}:{ProducerSettings.smartland_password}",
        "Content-Type": "application/json"
    }

    producer_data = {
        "reading_meter_number": '9',
        "meter_number": '745874857',
        "readingDate": datetime.fromisoformat('2025-09-05').isoformat()
    }

    # Asynchrone Anfrage an den Producer senden
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(producer_url, json=producer_data, headers=headers)
            print(response.status_code)

            if response.status_code == 200:
                print("Successfully sent data to producer.")
                return JSONResponse([], status_code=status.HTTP_200_OK)
            else:
                print(f"Producer responded with status code {response.status_code}.")
                print(response.json())
                return JSONResponse([], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"An error occurred while sending data to producer: {e}")
            return JSONResponse([], status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
