"""
Database configuration and connection management.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')


class DatabaseConfig:
    """Database configuration class."""
    
    def __init__(self):
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.database_name = os.environ.get('DB_NAME', 'stima_sacco')
        self._client = None
        self._database = None

    @property
    def client(self) -> AsyncIOMotorClient:
        """Get MongoDB client instance."""
        if self._client is None:
            self._client = AsyncIOMotorClient(self.mongo_url)
        return self._client

    @property
    def database(self):
        """Get database instance."""
        if self._database is None:
            self._database = self.client[self.database_name]
        return self._database

    async def close_connection(self):
        """Close database connection."""
        if self._client:
            self._client.close()


# Global database instance
db_config = DatabaseConfig()


def get_database():
    """Get database instance."""
    return db_config.database


async def close_database_connection():
    """Close database connection."""
    await db_config.close_connection()

