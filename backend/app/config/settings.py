"""
Application configuration settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')


class AppConfig:
    """Application configuration class."""
    
    # API Configuration
    API_TITLE = "Stima Sacco Debt Management System"
    API_VERSION = "1.0.0"
    API_PREFIX = "/api"
    
    # Database Configuration
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    DATABASE_NAME = os.environ.get('DB_NAME', 'stima_sacco')
    
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    
    # CORS Configuration
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
    ]
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # External Integrations
    PROFIX_API_URL = os.environ.get('PROFIX_API_URL', '')
    PROFIX_API_KEY = os.environ.get('PROFIX_API_KEY', '')


# Global configuration instance
app_config = AppConfig()

