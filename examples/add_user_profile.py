from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from database import EngineSingleton, setup_db
from database.workout_routine_db import UserProfile

load_dotenv()

engine = EngineSingleton.get_instance()
setup_db(engine)

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

minnie = UserProfile(
    age=27,
    weight=70,
    experience_level="intermediate",
    activity_level="moderate"
)

session.add(minnie)
session.commit()
