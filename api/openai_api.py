import os
import logging

from models import WorkoutRoutine

from openai import OpenAI

log = logging.getLogger(__name__)

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_gpt_prompt(user_query, notes, user_profile):
    clean_notes = "\n".join([n for n in notes if n])
    # log.debug("gen_gpt_user_prompt: %r, %r", notes, user_profile)

    return [
        {
            "role": "system",
            "content": "You are a fitness expert specializing in weightlifting.",
        },
        {
            "role": "user",
            "content": f"""
                User Profile:
                    Age: {user_profile['age']},
                    Weight: {user_profile['weight']} kg,
                    Gender: {user_profile['gender']}
                Experience:
                    {user_profile['experience_level']},
                Activity Level:
                    {user_profile['activity_level']}
                Goal: {user_profile['goal']}
                Notes: {clean_notes}

                User Question: {user_query}

                Provide a detailed response in the requested format
            """
        }
    ]


def get_gpt_response(user_query, notes, user_profile):
    """
    Fetch a response from OpenAI GPT based on user query and profile.
    """
    try:
        gpt_prompt = get_gpt_prompt(user_query, notes, user_profile)
        log.debug("gpt prompt: %r", gpt_prompt)

        # Call GPT API
        with client.beta.chat.completions.stream(
            model="gpt-4o",
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
        print("JRMJRM0")
        print("Final completion:", final_completion.to_json())

        if final_completion.choices[0].message.refusal:
            raise Exception(final_completion.choices[0].message.refusal)

        print("JRMJRM1")
        print("Final completion:(model_dump_json):",
              final_completion.choices[0].message.to_dict()["parsed"])
        print("JRMJRM2")
        print("Final completion:(message.model_dump_json):",
              final_completion.choices[0].message.model_dump_json(indent=4))
        print("JRMJRM3")
        print("Final completion:(message.parsed):",
              final_completion.choices[0].message.parsed)
        print("JRMJRM4")
        return final_completion.choices[0].message.to_dict()["parsed"]

        # workout_routine = completion.choices[0].message
        # if workout_routine.refusal:
        #     raise Exception(completion.refusal)
        #
        # return workout_routine.parsed

    except Exception as e:
        return f"Error: {str(e)}"
