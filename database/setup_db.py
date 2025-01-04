import os

from sqlalchemy import create_engine
from database.workout_routine_db import Base

class EngineSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if EngineSingleton._instance is None:
            EngineSingleton._instance = create_engine(
                os.getenv("DATABASE_URL"), echo=True
            )
        return EngineSingleton._instance


# Access the single engine instance
"""
engine = EngineSingleton.get_instance()
with engine.connect() as connection:
    result = connection.execute("SELECT 'Hello, Singleton!'")
    print(result.all())
"""

def setup_db(engine): Base.metadata.create_all(engine)

