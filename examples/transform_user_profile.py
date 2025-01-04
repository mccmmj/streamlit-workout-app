from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from database import EngineSingleton
from database.workout_routine_db import UserProfile
from models.workout_routine import UserProfile as UserProfileSchema

load_dotenv()

engine = EngineSingleton.get_instance()

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

stmt = select(UserProfile).where(UserProfile.age.__gt__(0))

for userProfile in session.query(UserProfile).all():
    userProfileSchema = UserProfileSchema.model_validate(userProfile)
    print(userProfileSchema)
