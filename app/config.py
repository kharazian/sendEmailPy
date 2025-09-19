import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
  MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
  MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
  MAIL_FROM: str = os.getenv("MAIL_FROM")
  MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
  MAIL_SERVER: str = os.getenv("MAIL_SERVER")
  MAIL_TLS: bool = os.getenv("MAIL_TLS", "True").lower() in ("true", "1", "t")
  MAIL_SSL: bool = os.getenv("MAIL_SSL", "False").lower() in ("true", "1", "t")
  USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "True").lower() in ("true", "1", "t")
  VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS", "True").lower() in ("true", "1", "t")

settings = Settings()