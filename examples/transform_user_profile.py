import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import setup_logging
from database import EngineSingleton, setup_db
from database import UserProfile
from models import UserProfile as UserProfileModel

setup_logging()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)

session = Session(engine)

stmt = select(UserProfile)
print(stmt)
result = session.execute(stmt)
print(f"{result=}")
print(result.all())
for user_profile_obj in result.all():
    userProfileModel = UserProfileModel.model_validate(user_profile_obj)
    log.info("userProfileModel=%r", userProfileModel)
