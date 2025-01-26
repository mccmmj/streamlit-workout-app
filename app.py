import logging
import streamlit as st

from utils import setup_logging
from database import EngineSingleton, setup_db

setup_logging()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)


def main():
    # Define a navigation widget in your entrypoint file
    pg = st.navigation([
        st.Page("screens/home.py", title="Home", default=True),
        st.Page("screens/workout_generator.py", title="Workout Generator"),
        st.Page("screens/workout_routines.py", title="Workout Routines"),
    ])
    pg.run()


if __name__ == "__main__":
    main()
