import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import setup_logging
from database import EngineSingleton, setup_db
from database import UserProfile
from database import Goal
from models import UserProfileCreate, UserProfile as UserProfileModel
from models import GoalCreate, Goal as GoalModel

setup_logging()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)

session = Session(engine)

# Create UserProfile
minnie = UserProfileCreate(
    name="minnie",
    age=27,
    weight="170 lbs",
    gender="Male",
    experience_level="intermediate",
    activity_level="moderate"
)

userProfile = UserProfile(**minnie.__dict__)

session.add(userProfile)
session.commit()
session.refresh(userProfile)
print(f"{userProfile=}")

goal = Goal(
    text="Muscle Gain",
    choices=[
        "Weight Loss",
        "Muscle Gain",
        "Improving Balance",
        "Build Strength",
        "Toning Up",
        "Boosting Energy",
        "Improving Sleep",
        "Improving mood and self-confidence",
        "Lowering the risk of many health  conditions",
        "Increasing resting metabolism",
    ],
    user_profile_id=userProfile.id
)

session.add(goal)
session.commit()
session.refresh(goal)
print(f"{goal=}")

# Retrieve user profile
stmt = select(UserProfile)
print(stmt)
result = session.execute(stmt)
print(f"{result=}")
print(result.all())
for user_profile_obj in result.all():
    userProfileModel = UserProfileModel.model_validate(user_profile_obj)
    log.info("userProfileModel=%r", userProfileModel)

# Retrieve goal
