from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

origins = [
    "http://localhost:4500",  # Frontend running on localhost:5500
    "http://127.0.0.1:4500",  # Alternative localhost address
]

# Add CORS middleware to allow specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only specified origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define 48 predefined questions with associated personality types
questions = [
    {"question": "Keep shipping and receiving records", "personality": "Conventional"},
    {"question": "Handle customers bank transactions", "personality": "Conventional"},
    {"question": "Operate a calculator", "personality": "Conventional"},
    {"question": "Compute and record statistical and other numerical data", "personality": "Conventional"},
    {"question": "Maintain employee records", "personality": "Conventional"},
    {"question": "Use a computer program to generate customer bills", "personality": "Conventional"},
    {"question": "Inventory supplies using a hand-held computer", "personality": "Conventional"},
    {"question": "Generate the monthly payroll checks for an office", "personality": "Conventional"},
    {"question": "Run a toy store", "personality": "Enterprising"},
    {"question": "Sell houses", "personality": "Enterprising"},
    {"question": "Manage a clothing store", "personality": "Enterprising"},
    {"question": "Manage a department within a large company", "personality": "Enterprising"},
    {"question": "Operate a beauty salon or barber shop", "personality": "Enterprising"},
    {"question": "Manage the operations of a hotel", "personality": "Enterprising"},
    {"question": "Sell merchandise at a department store", "personality": "Enterprising"},
    {"question": "Sell restaurant franchises to individuals", "personality": "Enterprising"},
    {"question": "Help elderly people with their daily activities", "personality": "Social"},
    {"question": "Teach children how to read", "personality": "Social"},
    {"question": "Supervise the activities of children at a camp", "personality": "Social"},
    {"question": "Help people with family-related problems", "personality": "Social"},
    {"question": "Teach an individual an exercise routine", "personality": "Social"},
    {"question": "Help people who have problems with drugs or alcohol", "personality": "Social"},
    {"question": "Do volunteer work at a non-profit organization", "personality": "Social"},
    {"question": "Give career guidance to people", "personality": "Social"},
    {"question": 'Design sets for plays', 'personality': 'Artistic'},
    {"question": 'Perform stunts for a movie or television show', 'personality': 'Artistic'},
    {"question": 'Play musical instrument', 'personality': 'Artistic'},
    {"question": 'Write books or plays', 'personality': 'Artistic'},
    {"question": 'Write a song', 'personality': 'Artistic'},
    {"question": 'Design art work for magazines', 'personality': 'Artistic'},
    {"question": 'Direct a play', 'personality': 'Artistic'},
    {"question": 'Conduct a musical choir', 'personality': 'Artistic'},
    {"question": "Make a map of the bottom of an ocean","personality":"Investigative"},
    {"question": "Work in a biology lab","personality":"Investigative"},
    {"question": "Study whales and other types of marine life","personality":"Investigative"},
    {"question": "Conduct biological research","personality":"Investigative"},
    {"question": "Develop a new medical treatment or procedure","personality":"Investigative"},
    {"question": "Do research on plants or animals","personality":"Investigative"},
    {"question": "Study animal behaviour","personality":"Investigative"},
    {"question": "Study the structure of the human body","personality":"Investigative"},
    {"question": "Install flooring in houses","personality":"Realistic"},
    {"question": "Assemble products in a factory","personality":"Realistic"},
    {"question": "Fix a broken faucet","personality":"Realistic"},
    {"question": "Operate a grinding machine in a factory","personality":"Realistic"},
    {"question": "Assemble electronic parts","personality":"Realistic"},
    {"question": "Work on an offshore oil-drilling rig","personality":"Realistic"},
    {"question": "Lay brick or tile","personality":"Realistic"},
    {"question": "Test the quality of parts before shipment","personality":"Realistic"}
]

# Store user responses temporarily
user_responses = []
current_index = 0

class Answer(BaseModel):
   response: int  # Answer on a scale from 1 to 5

@app.get("/start_test")
def start_test():
   """Reset and start the test."""
   global current_index, user_responses
   current_index = 0
   user_responses = []  # Reset responses
   return {
       **{"message" : f"Test started."}, 
       **{"next_question" : questions[current_index]["question"]}
   }

@app.post("/submit_answer")
def submit_answer(answer: Answer):
    """Store response and proceed to the next question."""
    global current_index

    if current_index >= len(questions):
        return {"message": "All questions answered", "completed": True}

    # Store the user's response
    user_responses.append({
        "question": questions[current_index]["question"],
        "personality": questions[current_index]["personality"],  # Corrected key
        "response": answer.response
    })

    current_index += 1

    # If all questions are answered, process results
    if current_index >= len(questions):
        return process_results()

    return {"message": "Answer recorded", "next_question": questions[current_index]["question"]}

def process_results():
    """Send responses to LLM to analyze personality type."""
    prompt = f"""
    You are a psychology expert analyzing a RIASEC personality test.
    The user answered {len(user_responses)} questions on a scale from 1 to 5.
    Each question is linked to one of six personality types: 
    Realistic, Investigative, Artistic, Social, Enterprising, or Conventional.

    Responses:
    {user_responses}

    Task:
    - Sum the scores for each personality type.
    - Identify the dominant personality type based on the highest score.
    - Return only the dominant personality type(s) in the format:
      Dominant Personality Type: [Type]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a psychology expert."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the raw text from OpenAI's response
        raw_output = response["choices"][0]["message"]["content"].strip()
        
        # Extract the personality type using regex
        import re
        match = re.search(r"Dominant Personality Type: (.+)", raw_output)
        
        if match:
            dominant_type = match.group(1).strip()
        else:
            dominant_type = "Could not determine personality type"

        return {
            "message": "Assessment complete",
            "personality": dominant_type,
            "completed": True
        }

    except Exception as e:
        return {
            "error": str(e)
        }
