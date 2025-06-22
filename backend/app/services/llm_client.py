# # app/services/llm_client.py
# import os
# import httpx
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
# GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# HEADERS = {
#     "Authorization": f"Bearer {GROQ_API_KEY}",
#     "Content-Type": "application/json"
# }

# async def call_groq(prompt: str) -> str:
#     payload = {
#         "model": GROQ_MODEL,
#         "messages": [
#             {"role": "system", "content": "You are Schema Generator Pro. You will generate ERD insights based on user business requirements and ERP metadata."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.3
#     }

#     async with httpx.AsyncClient() as client:
#         response = await client.post(GROQ_URL, headers=HEADERS, json=payload)
#         response.raise_for_status()
#         result = response.json()
#         return result['choices'][0]['message']['content']

# app/services/llm_client.py

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

async def call_groq(prompt: str, system_message: str = "You are Schema Generator Pro. You will generate ERD insights based on user business requirements and ERP metadata.") -> str:
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROQ_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
