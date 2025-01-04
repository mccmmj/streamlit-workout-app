# streamlit-workout-app
StreamLit Python Workout App  

This is a minimal research and investigation app
that demonstrates the use structured outputs provided by Openai.
The intent was to facilitate the persistence and retreival
of responses generated from AI prompts provided from various
screens presented to the user.

# Installation
pipenv --python 3.12
pipenv run poetry install

# Configuration
Create `.env` file with the following content:  
```
ANTHROPIC_API_KEY=<your anthropic api key>
OPENAI_API_KEY=<your openai api key>
API_PROVIDER=OPENAI # ANTHROPIC|OPENAI
LOG_LEVEL=INFO
DATABASE_URL="sqlite:///data/workout.db"
```
> Currently only API_PROVIDER=OPENAI is supported

# Execution
streamlit run app.py

# Operation
The app is minimal.  Three screens, home, workout routines, and workout generator.
Home:
The Home screen allows you to select a user profile

Workout Routines:
The Workout Routines screen allows you to select the range of workout routines in the database.

Workout Generator:
The Workout Generator screen allows you to specify any workout conditions  you have and 
input a prompt.

Example of notes are:
    "I have no injuries"
    "I prefer free weights"
    "I don't like lunges"

Examples of prompts are:
   "What is the best legs workout routine for me?",
   "What is the best core workout routine for me?"

# Miscellany
Add support for user management.  
Add Screens for exercises and data entry.  
Add more agents to support exercise tracking, analysis and charts.  
Replace streamlit with React-native or other mobile app framework.  
