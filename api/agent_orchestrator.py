import logging
import openai
import json

from openai import OpenAI
from config.settings import settings
from models import WorkoutRoutine
from api.agent import get_workout_routine


log = logging.getLogger(__name__)

# Create an OpenAI client
# MODEL_NAME = "gpt-4o-2024-08-06"
# MODEL_NAME = "gpt-4o-2024-05-13"
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def agent_orchestrator(prompt):
    messages = [{"role": "user", "content": prompt}]
    tools_list = [
        {
            "type": "function",
            "function": {
                "name": "get_workout_routine",
                "description": "generate workout routines based on user query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "Focus and goal of workout routine",
                        },
                    },
                    "required": ["user_query"],
                    "additionalProperties": False
                },
                "strict": True
            },
        }
    ]
    response = client.chat.completions.create(
        model=settings.MODEL_NAME, messages=messages, tools=tools_list, tool_choice='auto')
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    log.debug("agent_orchestrator: tool_calls=%r", tool_calls)
    # check if the model wants to call a function
    if tool_calls:
        available_functions = {
            "get_workout_routine": get_workout_routine,
        }  # you can have multiple functions here

        # extend conversation with assistant's reply
        messages.append(response_message)

        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name == 'get_workout_routine':
                function_response = function_to_call(
                    user_query=function_args.get("user_query"),
                )
                log.info("In agent_orchestrator: function_response=%r", function_response)
            else:
                raise Exception(f"Unknown function to call: {function_name}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": function_response,
                }
            )  # extend conversation with function responses

            # # Orig
            # second_response = client.chat.completions.create(
            #     model=settings.MODEL_NAME,
            #     messages=messages,
            #     tools=tools_list
            # )  # get a new response from the model where it can see the function response
            # Call GPT API
            second_response = client.beta.chat.completions.parse(
                model=settings.MODEL_NAME,
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
                response_format=WorkoutRoutine,
            )
            return second_response.choices[0].message.content
    else:
        return response_message.content
