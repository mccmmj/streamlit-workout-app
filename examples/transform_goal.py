import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import setup_logging
from database import EngineSingleton, setup_db
from database import Goal
from models import Goal as GoalModel

setup_logging()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)

session = Session(engine)

stmt = select(Goal)
print(stmt)
result = session.execute(stmt)
print(f"{result=}")
print(result.all())
for goal_obj in result.all():
    goalModel = GoalModel.model_validate(goal_obj)
    log.info("goalModel=%r", goalModel)
