from fastapi import FastAPI, HTTPException
from app.services import email_service
from app.schemas.email import Appointment

app = FastAPI()

@app.get("/")
def read_root():
  return {"message": "Email service is running. "}

@app.post("/send-appointment")
async def send_appointment_endpoint(appointment: Appointment):
  try:
      await email_service.send_appointment_email(appointment)
      return {"message": "Appointment invitations sent successfully."}
  except Exception as e:
      raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")