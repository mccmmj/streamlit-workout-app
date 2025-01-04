from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from database import EngineSingleton, setup_db
from database.workout_routine_db import UserProfile
from models.workout_routine import UserProfileCreate
from models.workout_routine import UserProfile as UserProfileSchema

load_dotenv()

engine = EngineSingleton.get_instance()
setup_db(engine)

# Create UserProfile
minnie = UserProfileCreate(
    age=27,
    weight="170 lbs",
    experience_level="intermediate",
    activity_level="moderate"
)

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

userProfile = UserProfile(**minnie)
session.add(userProfile)
session.commit()
session.refresh(userProfile)

