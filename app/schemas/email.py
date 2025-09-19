from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class Attendee(BaseModel):
    email: str

class Appointment(BaseModel):
    from_email: EmailStr = Field(..., alias="from") # Use from_email to avoid conflicts with Python keyword 'from'
    to: Optional[List[EmailStr]] = None
    subject: str
    html: str
    method: str
    ics_text: str = Field(..., alias="icsText")
    ics_attendee_text: Optional[str] = Field(None, alias="icsAttendeeText")