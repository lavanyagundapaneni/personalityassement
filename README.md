# Personality Assessment AI Agent

This project is an AI-based personality assessment agent built using FastAPI and OpenAI's GPT-4 Turbo model. The agent conducts a RIASEC personality test by presenting predefined questions to the user and analyzing their responses to determine their dominant personality type.

## Technologies Used
* **FastAPI** (Python Web Framework)

* **Pydantic** (Data validation and serialization)

* **OpenAI GPT-4** Turbo (LLM for personality analysis)

* **Dotenv** (Environment variable management)

* **CORS Middleware** (For handling cross-origin requests)

## Features
* Conducts a RIASEC personality test

* 48 predefined questions mapped to six personality types:

       Realistic

       Investigative

       Artistic

       Social

       Enterprising

       Conventional

* Collects user responses on a scale from 1 to 5

* Processes responses to calculate the dominant personality type

* Uses OpenAI's GPT-4 Turbo to analyze and determine the final personality type

## Installation
### 1. Prerequisites 
* Python 3.8+
* An OpenAI API key

### 2. Setup Instructions
1. Clone Repository
   ```
   git clone https://github.com/your-repo/personality-assessment-agent.git
   cd personality-assessment-agent
  ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables
  ```
   OPENAI_API_KEY=your_openai_api_key_here
  ```
4. Run the FastAPI server
  ```
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
  
