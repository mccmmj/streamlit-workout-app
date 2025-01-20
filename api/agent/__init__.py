from config.settings import settings
from ._anthropic.workout_routine import get_workout_routine as _get_workout_routine_anthro
from ._openai.workout_routine import get_workout_routine as _get_workout_routine_openai


def get_workout_routine(user_query, notes=None, user_profile=None):
    if settings.API_PROVIDER == "ANTHROPIC":
        return _get_workout_routine_anthro(user_query, notes, user_profile)
    if settings.API_PROVIDER == "OPENAI":
        return _get_workout_routine_openai(user_query, notes, user_profile)

    raise Exception("Unknown API provider, ensure API_PROVIDER=ANTROPIC|OPENAI")
