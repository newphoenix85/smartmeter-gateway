from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Annotated
import base64
from app.internal.settings import ProducerSettings
from app.cruds import user_crud, smartland_consumer_crud
from app.schemas.smartland_smgw_schema import ISmartlandSMGWCreate
from app.models.smartland_smgw_model import SmartlandSMGW
from uuid import uuid4
from datetime import datetime

router = APIRouter(
    prefix="/api/m2m",
    tags=["m2m"]
)

async def verify_basic_auth(authorization: Annotated[str | None, Header()] = None):
    # SECURITY PRINCIPLE: Identification & Authentication
    # Verify strict Machine-to-Machine credentials to ensuring only authorized consumers can push data.
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization Header")
    
    try:
        scheme, credentials = authorization.split()
        if scheme.lower() != 'basic':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authentication Scheme")
            
        decoded = base64.b64decode(credentials).decode("utf-8")
        username, password = decoded.split(":")
        
        if username != ProducerSettings.smartland_username or password != ProducerSettings.smartland_password:
             import logging
             logging.warning(f"SECURITY EVENT (M2M): Failed login attempt for user '{username}'. Invalid credentials.")
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
             
    except Exception:
        import logging
        logging.warning("SECURITY EVENT (M2M): Malformed Authorization Header received.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization Header")

@router.post("/add")
async def add_reading_m2m(
    body: dict,
    auth: None = Depends(verify_basic_auth)
):
    """
    M2M Endpoint to receive reading values from the Smart Meter Gateway.
    Secured via Basic Auth (Consumer -> Producer).
    """
    try:
        # Check if user exists or create dummy user for the gateway if needed. 
        # In a real scenario, the gateway would send the user_id or we map it.
        # Here we assume the input body contains necessary identification or we use a tech user.
        
        # For this implementation, we expect the gateway to send the reading.
        # The Consumer sends the full SmartlandSMGW schema: id, value, meter_id, ts, user_id, obis, unit
        
        reading_id = body.get('id', str(uuid4()))
        
        # Basic Input Validation
        if 'value' not in body or 'meter_id' not in body or 'ts' not in body:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required fields")

        reading_meter_number = int(body['value'])
        meter_number = int(body["meter_id"])
        readingDate = datetime.fromisoformat(body['ts'])
        obis = body.get('obis', '1-0:18.0.1')
        unit = body.get('unit', 'kWh')
        
        # SECURITY PRINCIPLE: Input Validation
        if reading_meter_number < 0:
             import logging
             logging.warning(f"SECURITY EVENT (M2M): Invalid input attempt. "
                             f"Negative reading_meter_number: {reading_meter_number}. "
                             f"Provided User ID: {body.get('user_id')}")
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Negative reading value")
        
        # Use provided user_id or fallback (potentially unsafe, but for demo/testing)
        # ideally we should lookup user by meter_number.
        user_id = body.get('user_id')
        
        if not user_id:
            # Fallback: Create or get a default 'm2m_import_user' or fail.
            # For the purpose of the demo where we want to see data:
            # We will create a dummy user if not provided.
             user_id = "m2m-imported-user"
        
        # We need to make sure this user exists in the producer DB so foreign key constraints don't fail?
        # The User table exists.
        # Let's try to ensure the user exists.
        try:
             # minimal user payload
             user_payload = {
                 "sub": user_id,
                 "email": "m2m@smartland.lan",
                 "email_verified": True,
                 "name": "M2M Import",
                 "given_name": "M2M",
                 "preferred_username": "m2m",
                 "nickname": "m2m",
                 "groups": [],
                 "auth_time": 0,
                 "iss": "",
                 "aud": "",
                 "exp": 0,
                 "iat": 0,
                 "acr": ""
             }
             db_user = await user_crud.create(obj_in=user_payload)
        except Exception as e:
            print(f"User creation/fetch failed: {e}")
            # If user creation fails, maybe they exist. Continue.

        db_response = await smartland_consumer_crud.create(
            obj_in=ISmartlandSMGWCreate(
                id=reading_id,
                user_id=user_id, # Use the ID we determined
                ts=readingDate,
                value=reading_meter_number,
                meter_id=meter_number,
                obis=obis,
                unit=unit
            )
        )
        
        return {"status": "success", "id": reading_id}

    except Exception as ex:
        print(f"M2M Error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))
