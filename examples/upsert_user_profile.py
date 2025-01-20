import logging

from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import setup_logging
from database import upsert_user_profile, upsert_goal, upsert_note
from database import EngineSingleton, setup_db
from database import UserProfile
from database import Goal
from database import Note
from models import UserProfileCreate, UserProfile as UserProfileModel
from models import GoalCreate, Goal as GoalModel
from models import NoteCreate, Note as NoteModel

setup_logging()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)

# Create UserProfile
minnie = UserProfileCreate(
    name="minnie",
    age=27,
    weight="125 lbs",
    gender="Female",
    experience_level="Intermediate",
    activity_level="Moderate"
)

session = Session(engine)
userProfile = upsert_user_profile(session, minnie.__dict__)
log.info(f"{userProfile=}")
session.commit()

userProfileModel = UserProfileModel.model_validate(userProfile)
log.info(f"{userProfileModel=}")

# Retrieve user goal
gStmt = select(Goal).where(Goal.user_profile_id == userProfile.id)
gResult = session.scalars(gStmt)
log.info(f"{gResult=}")
log.info(gResult.all())
tmpGoal = gResult.all()[0] if gResult and gResult.all() else None
goalModel: Optional[GoalModel] = None
if tmpGoal:
    goalModel = GoalModel.model_validate(tmpGoal)
else:
    goalModel = GoalModel(
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
    )

## This should either insert or update the goal with same values
goal = upsert_goal(session, dict(
    id=goalModel.id,
    text=goalModel.text,
    choices=goalModel.choices,
    user_profile_id=userProfile.id)
)
log.info(f"{goal=}")
session.commit()

goalModel = GoalModel.model_validate(goal)
print(f"{goalModel=}")

# Retrieve user notes
nStmt = select(Note).where(Note.user_profile_id == userProfile.id)
nResult = session.scalars(nStmt)
print(f"{nResult=}")
print(nResult.all())
tmpNote = nResult.all()[0] if nResult and nResult.all() else None
noteModel: Optional[NoteModel] = None
if tmpNote:
    noteModel = NoteModel.model_validate(tmpNote)
else:
    text_items = ["I don't like lunges", "I prefer free weights"]
    noteModel = NoteModel(
        text="\n".join(text_items),
    )

note = upsert_note(session, dict(
    text=noteModel.text,
    user_profile_id=userProfile.id)
)
print(f"{note=}")
session.commit()

noteModel = NoteModel.model_validate(note)
print(f"{noteModel=}")

# Retrieve user profile
uStmt = select(UserProfile)
print(uStmt)
result = session.scalars(uStmt)
print(f"{result=}")
print(result.all())
for user_profile_obj in result.all():
    userProfileModel = UserProfileModel.model_validate(user_profile_obj)
    log.info("userProfileModel=%r", userProfileModel)
