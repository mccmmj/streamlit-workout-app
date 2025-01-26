import logging

from openai import OpenAI

import streamlit as st

from models import WorkoutRoutine
from config.settings import settings

log = logging.getLogger(__name__)

# Set up OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def _get_gpt_prompt(user_query, goal, notes, user_profile):
    clean_notes = "\n".join([n for n in notes if n])
    log.debug("In _get_gpt_prompt: %r, %r, %r", goal, notes, user_profile)

    return [
        {
            "role": "system",
            "content": "You are a fitness expert specializing in weightlifting.",
        },
        {
            "role": "user",
            "content": f"""
                User Profile:
                    Name: {user_profile.name},
                    Age: {user_profile.age},
                    Weight: {user_profile.weight},
                    Gender: {user_profile.gender},
                Experience:
                    {user_profile.experience_level},
                Activity Level:
                    {user_profile.activity_level},
                Goal: {goal},
                Notes: {clean_notes},

                User Question: {user_query}

                Provide a detailed response in the requested format
            """
        }
    ]


def get_workout_routine(user_query, goal=None, notes=None, user_profile=None):
    """
    Fetch a response from OpenAI GPT based on user query and profile.
    """
    log.debug("In get_workout_routine: user_query: %s", user_query)
    try:
        if not goal and 'shared_goal' in st.session_state:
            goal = st.session_state.shared_goal
        if not notes and 'shared_notes' in st.session_state:
            notes = st.session_state.shared_notes
        if not user_profile and 'shared_user_profile' in st.session_state:
            user_profile = st.session_state.shared_user_profile

        gpt_prompt = _get_gpt_prompt(user_query, goal, notes, user_profile)
        log.debug("In get_workout_routine: gpt_prompt: %r", gpt_prompt)
        print(f"{gpt_prompt=}")

        # Call GPT API
        with client.beta.chat.completions.stream(
            model=settings.MODEL_NAME,
            max_tokens=1024,
            temperature=0.7,
            messages=gpt_prompt,
            response_format=WorkoutRoutine,
        ) as stream:
            for event in stream:
                if event.type == "content.delta":
                    if event.parsed is not None:
                        # Print the parsed data as JSON
                        print("content.delta.parsed:", event.parsed)
                elif event.type == "content.done":
                    print("content.done")
                elif event.type == "error":
                    print("Error in stream:", event.error)

        final_completion = stream.get_final_completion()
        # print("JRMJRM0")
        # print("Final completion:", final_completion.to_json())

        if final_completion.choices[0].message.refusal:
            raise Exception(final_completion.choices[0].message.refusal)

        # print("JRMJRM1")
        # print("Final completion:(model_dump_json):",
        #       final_completion.choices[0].message.to_dict()["parsed"])
        # log.debug("JRMJRM2")
        # log.debug("Final completion:(message.model_dump_json):",
        #       final_completion.choices[0].message.model_dump_json(indent=4))
        return final_completion.choices[0].message.model_dump_json()
        # print("JRMJRM3")
        # print("Final completion:(message.parsed):",
        #       final_completion.choices[0].message.parsed)
        # print("JRMJRM4")
        return final_completion.choices[0].message.to_dict()["parsed"]

        # workout_routine = completion.choices[0].message
        # if workout_routine.refusal:
        #     raise Exception(completion.refusal)
        #
        # return workout_routine.parsed

    except Exception as e:
        return f"Error: {str(e)}"
