from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings
from app.schemas.email import Appointment
import html

conf = ConnectionConfig(
  MAIL_USERNAME=settings.MAIL_USERNAME,
  MAIL_PASSWORD=settings.MAIL_PASSWORD,
  MAIL_FROM=settings.MAIL_FROM,
  MAIL_PORT=settings.MAIL_PORT,
  MAIL_SERVER=settings.MAIL_SERVER,
  MAIL_STARTTLS=settings.MAIL_TLS,
  MAIL_SSL_TLS=settings.MAIL_SSL,
  USE_CREDENTIALS=settings.USE_CREDENTIALS,
  VALIDATE_CERTS=settings.VALIDATE_CERTS,
)

fm = FastMail(conf)

async def send_appointment_email(appointment: Appointment):
  ics_file = ("invitation.ics", appointment.ics_text.encode("utf-8"), "text/calendar")
  
  message_organizer = MessageSchema(
      subject=appointment.subject,
      recipients=[appointment.from_email],
      body=html.unescape(appointment.html), # Convert HTML entities
      attachments=[ics_file]
  )
  await fm.send_message(message_organizer)
 
  attendee_list = [attendee for attendee in appointment.to if attendee != appointment.from_email]
  if attendee_list:
      ics_attendee_file = ("invitation.ics", appointment.ics_attendee_text.encode("utf-8"), "text/calendar")
      
      message_attendee = MessageSchema(
          subject=appointment.subject,
          recipients=attendee_list,
          body=html.unescape(appointment.html),
          attachments=[ics_attendee_file]
      )
      await fm.send_message(message_attendee)