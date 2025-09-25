import html
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from app.config import settings
from app.schemas.email import Appointment

# --- Helper Functions for MIME parts ---

def create_html_part(html_content: str):
    """Creates a MIMEText part for HTML content."""
    return MIMEText(html.unescape(html_content), "html")

def create_ics_part(ics_text: str, method: str):
    """Creates a MIMEBase part for iCalendar content with a specified method."""
    ics_part = MIMEBase("text", f"calendar; method={method}")
    ics_part.set_payload(ics_text.encode('utf-8'))
    ics_part.add_header('Content-Type', f'text/calendar; method={method}; name="invite.ics"')
    ics_part.add_header('Content-Disposition', 'inline; filename="invite.ics"')
    encoders.encode_base64(ics_part)
    return ics_part

# --- Main Email Sending Function ---

async def send_appointment_email(appointment: Appointment):
    """
    Sends an appointment email to both the organizer and attendees.
    This version uses the synchronous smtplib library.
    """
    try:
        # Create common message parts
        html_part = create_html_part(appointment.html)

        # Create alternative part and attach the HTML
        alt_part = MIMEMultipart("alternative")
        alt_part.attach(html_part)

        # Create organizer and attendee specific ICS parts
        ics_organizer_part = create_ics_part(appointment.icsText, appointment.method)
        ics_attendee_part = create_ics_part(appointment.icsAttendeeText, appointment.method)

        # Build the organizer's email message
        organizer_msg = MIMEMultipart("mixed")
        organizer_msg["From"] = settings.MAIL_USERNAME
        organizer_msg["To"] = appointment.from_email
        organizer_msg["Subject"] = appointment.subject
        organizer_msg.attach(alt_part)
        organizer_msg.attach(ics_organizer_part)

        # Build the attendee's email message
        attendee_msg = MIMEMultipart("mixed")
        attendee_msg["From"] = settings.MAIL_USERNAME
        attendee_msg["To"] = ", ".join(appointment.to)
        attendee_msg["Subject"] = appointment.subject
        attendee_msg.attach(alt_part)
        attendee_msg.attach(ics_attendee_part)

        # Connect to the SMTP server and send the emails
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)

            # Send to the organizer
            server.sendmail(settings.MAIL_USERNAME, appointment.from_email, organizer_msg.as_string())

            # Send to all attendees
            server.sendmail(settings.MAIL_USERNAME, appointment.to, attendee_msg.as_string())

        print("Appointment emails sent successfully.")

    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")