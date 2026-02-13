import asyncio
from datetime import datetime
from uuid import uuid4
import httpx
from random import randint
import base64
import logging

from app.cruds import user_crud, smartland_smgw_crud, smartland_logbook_crud
from app.schemas.smartland_smgw_schema import ISmartlandSMGWCreate
from app.schemas.smartland_logbook_schema import ILogbookCreate
from app.internal import ProducerSettings

# Global state to keep track of meter values per user
# Dictionary mapping user_id -> last_meter_value
meter_states = {}

# Security Principles
# -------------------
# 
# 1. Authentifizierung:
#    - Der Simulator authentifiziert sich gegenüber dem Producer-Backend mittels Basic Auth via `ProducerSettings`.
# 2. Vertraulichkeit:
#    - Die Kommunikation mit dem Producer erfolgt über TLS/HTTPS.
# 3. Integrität:
#    - Generierung von eindeutigen IDs (UUIDs) und Zeitstempeln für jede Messung.
# 4. Verfügbarkeit:
#    - Fehlerbehandlung und Retries bei Verbindungsfehlern zum Producer.
# 5. Auditierung:
#    - Logging aller Aktionen und Fehler für Nachvollziehbarkeit.
# 6. Härtung (Hardening):
#    - Entwicklungsmodus: `verify=False` wird verwendet (in Produktion deaktivieren für vollständige Zertifikatsprüfung).

logger = logging.getLogger(__name__)

async def simulate_smart_meter_readings():
    """
    Background task to simulate a Smart Meter generating data every 10 minutes.
    Iterates through ALL users in the database to simulate data for each one.
    """
    global meter_states
    logger.info("Starting Smart Meter Simulator (Multi-User)...")
    
    while True:
        try:
            logger.info("Simulator: Tick")
            await asyncio.sleep(600) # Wait 1 minute
            
            # We use SessionLocal from database module which is already configured
            from app.database.database import SessionLocal
            from sqlalchemy import select
            from app.models.user_model import User
            
            async with SessionLocal() as session:
                 # 1. Fetch ALL users
                 result = await session.execute(select(User))
                 users = result.scalars().all()
                 
                 if not users:
                     logger.info("Simulator: No users found. Skipping reading generation.")
                     continue
                 
                 logger.info(f"Simulator: Found {len(users)} users. Generating data...")


                 # 2. Iterate over each user
                 for user in users:
                     try:
                         # Initialize state for new users
                         if user.id not in meter_states:
                             meter_states[user.id] = 10000 + randint(0, 5000) # Random start value
                         
                         # Check/Fix Meter ID (Migration for existing users without meter_id)
                         if not user.meter_id:
                             logger.info(f"Simulator: User {user.id} has no meter_id. Generating and saving...")
                             user.meter_id = int(str(int.from_bytes(user.id.encode(), 'little'))[:9])
                             session.add(user)
                             await session.commit()
                             await session.refresh(user)
                         
                         current_meter_id = user.meter_id

                         # 3. Generate Data
                         current_value = meter_states[user.id] + randint(1, 100) # Increment
                         meter_states[user.id] = current_value
                         
                         reading_id = str(uuid4())
                         timestamp = datetime.now()
                         
                         logger.info(f"Simulator: Generating reading {current_value} for user {user.id} (Meter: {current_meter_id})")
        
                         # 4. Store in Consumer DB
                         # We invoke CRUD but pass our manual session
                         await smartland_smgw_crud.create(
                            obj_in=ISmartlandSMGWCreate(
                                id=reading_id,
                                user_id=user.id,
                                ts=timestamp,
                                meter_id=current_meter_id, 
                                value=current_value,
                                obis='1-0:18.0.1',
                                unit='kWh'
                            ),
                            db_session=session
                         )
                         
                         # 5. Push to Producer
                         producer_url = "https://producer.smartland.lan/api/m2m/add"
                         headers = {
                            "Authorization": f"Basic {base64.b64encode(f'{ProducerSettings.smartland_username}:{ProducerSettings.smartland_password}'.encode()).decode()}",
                            "Content-Type": "application/json"
                         }
                         
                         producer_payload = {
                            "id": reading_id,
                            "value": current_value,
                            "meter_id": current_meter_id,
                            "ts": timestamp.isoformat(),
                            "user_id": user.id,
                            "obis": "1-0:18.0.1",
                            "unit": "kWh"
                         }
        
                         
                         async with httpx.AsyncClient(verify=False) as client:
                             resp = await client.post(producer_url, json=producer_payload, headers=headers)
                             if resp.status_code == 200:
                                 logger.info(f"Simulator: Pushed for user {user.id}.")
                             else:
                                 logger.error(f"Simulator: Push failed for user {user.id}: {resp.status_code} {resp.text}")

                     except Exception as user_e:
                         logger.error(f"Simulator: Error processing user {user.id}: {user_e}")
                         # Continue to next user even if one fails
                         continue

        except Exception as e:
            logger.error(f"Simulator Error: {e}")
            await asyncio.sleep(10) # Wait before retrying
