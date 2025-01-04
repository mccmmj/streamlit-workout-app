import os
import logging

from anthropic import Anthropic

from utils import SingletonMeta

log = logging.getLogger(__name__)


"""
EXAMPLE RESPONSE
Chatbot: [TextBlock(text="I'll create a detailed workout plan suitable for your age, experience level, and muscle-gaining goals.

3-Day Split Program (Rest days between workouts)

DAY 1 - PUSH
1. Chest/Shoulders/Triceps
- Dumbbell Bench Press: 3x8-10
- Seated Shoulder Press: 3x8-10
- Incline Dumbbell Press: 3x10-12
- Lateral Raises: 3x12-15
- Tricep Pushdowns: 3x12-15
- Face Pulls: 3x15 (shoulder health)

DAY 2 - PULL
1. Back/Biceps
- Assisted Pull-ups or Lat Pulldowns: 3x8-10
- Seated Cable Rows: 3x10-12
- Single-Arm Dumbbell Rows: 3x10-12
- Bicep Curls: 3x10-12
- Hammer Curls: 3x12-15
- Back Extensions: 2x15

DAY 3 - LEGS
1. Lower Body
- Goblet Squats: 3x10-12
- Romanian Deadlifts: 3x10-12
- Leg Press: 3x12-15
- Leg Extensions: 3x15
- Seated Leg Curls: 3x15
- Calf Raises: 3x15-20

Important Guidelines:
1. Warm-up: 5-10 minutes light cardio + dynamic stretching
2. Rest between sets: 90-120 seconds
3. Workout frequency: Allow 1-2 rest days between sessions
4. Progressive overload: Increase weight by 2-5% when you can complete all reps with good form

Nutrition Tips for Muscle Gain:
- Protein: 1.6-2.0g per kg body weight (123-154g daily)
- Caloric surplus: 300-500 calories above maintenance
- Focus on whole foods
- Stay hydrated (2-3 liters daily)

Recovery Recommendations:
- 7-8 hours sleep
- Light stretching on rest days
- Consider fish oil supplements for joint health
- Monitor recovery - adjust volume if needed

Start with lighter weights to perfect form and gradually increase intensity. Listen to your body and adjust as needed. Consider working with a trainer initially to ensure proper form.", type='text')]
"""


class ApiClient(metaclass=SingletonMeta):
    def __init__(self):
        self.client = Anthropic()


def get_gpt_response(user_query, notes, user_profile):
    """
    Fetch a response from OpenAI GPT based on user query and profile.
    """
    try:
        # Call GPT API
        client = ApiClient().client
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,
            system="You are a fitness expert specializing in weightlifting.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""
                                User Profile:
                                   Age: {user_profile['age']},
                                   Weight: {user_profile['weight']} kg,
                                Experience:
                                    {user_profile['experience']},
                                Activity Level:
                                    {user_profile['activity_level']}, "
                                Goal: {user_profile['goal']}
                             """,
                        },
                        {"type": "text", "text": f"User Question: {user_query}"},
                        {"type": "text", "text": "Provide a detailed response"},
                    ],
                },
            ],
        )
        return message.content

    except Exception as e:
        return f"Error: {str(e)}"
