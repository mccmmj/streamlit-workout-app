import os

from api import anthropic_api
from api import openai_api


def get_gpt_response(user_query, notes, user_profile):
    if os.getenv("API_PROVIDER") == "ANTHROPIC":
        return anthropic_api.get_gpt_response(user_query, notes, user_profile)
    if os.getenv("API_PROVIDER") == "OPENAI":
        return openai_api.get_gpt_response(user_query, notes, user_profile)

    raise Exception("Unknown API provider, ensure API_PROVIDER=ANTROPIC|OPENAI")
