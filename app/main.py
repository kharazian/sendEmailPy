from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.services import email_service
from app.services import auth_service
from app.schemas.email import Appointment
from app.schemas.user import User

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def read_root():
  return {"message": "Email service is running. "}
 
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await auth_service.authenticate_user(form_data)

@app.post("/send-appointment")
async def send_appointment_endpoint(appointment: Appointment, current_user: User = Depends(auth_service.get_current_user)):
  try:
      await email_service.send_appointment_email(appointment)
      return {"message": "Appointment invitations sent successfully."}
  except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")