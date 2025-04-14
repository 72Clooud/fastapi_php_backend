from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    
    db_user: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str
    
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"
        
settings = Settings()