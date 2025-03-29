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
