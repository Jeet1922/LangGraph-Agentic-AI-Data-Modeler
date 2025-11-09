# # app/services/llm_client.py
# import os
# import httpx
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Updated to supported model
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
# Use a currently supported model - updated to newer models
# Users can override with GROQ_MODEL env var, but we default to a known working model
env_model = os.getenv("GROQ_MODEL")
# List of decommissioned/unsupported models to avoid
decommissioned_models = [
    "llama3-70b-8192", 
    "llama-3.3-70b-versatile", 
    "llama3-8b-8192",
    "llama-3.1-70b-versatile",  # Also decommissioned
    "mixtral-8x7b-32768",       # Decommissioned
    "llama-3.2-11b-vision-preview",  # Decommissioned
    "llama-3.2-3b-preview",          # Decommissioned
    "llama-3.2-90b-vision-preview",  # Decommissioned
    "gemma2-9b-it"                   # Decommissioned
]
# Try newer supported model names (as of 2025)
# Note: Model availability changes, so we prioritize stable models
# Tested and confirmed working: llama-3.1-8b-instant
supported_models = [
    "llama-3.1-8b-instant",          # ✅ CONFIRMED WORKING - Fast and stable
    "llama-3.3-70b-versatile",       # Original model (if it becomes available again)
    "mixtral-8x7b-32768",            # Mixtral model (if available)
]

if env_model and env_model not in decommissioned_models:
    GROQ_MODEL = env_model
else:
    # Default to llama-3.1-8b-instant - confirmed working via test script
    GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def _call_groq_with_model(prompt: str, system_message: str, model_name: str) -> str:
    """
    Internal function to call Groq API with a specific model.
    """
    # Build headers dynamically
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare payload
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(GROQ_URL, headers=headers, json=payload)
        
        # Check for errors
        if response.status_code != 200:
            error_text = response.text
            try:
                error_json = response.json()
                error_message = error_json.get("error", {}).get("message", error_text)
                error_type = error_json.get("error", {}).get("type", "unknown_error")
                error_code = error_json.get("error", {}).get("code", "")
                # Return error info for fallback handling
                return None, f"Groq API error ({response.status_code}) with model '{model_name}': {error_message} (type: {error_type}, code: {error_code})"
            except:
                return None, f"Groq API error ({response.status_code}) with model '{model_name}': {error_text}"
        
        result = response.json()
        
        # Validate response structure
        if "choices" not in result or len(result["choices"]) == 0:
            return None, "Invalid response from Groq API: no choices found"
        
        return result['choices'][0]['message']['content'], None

async def call_groq(prompt: str, system_message: str = "You are Schema Generator Pro. You will generate ERD insights based on user business requirements and ERP metadata.") -> str:
    """
    Call Groq API with improved error handling and validation.
    Includes fallback to alternative models if the primary model fails.
    """
    # Validate API key
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your .env file or environment variables.")
    
    if GROQ_API_KEY == "None" or len(GROQ_API_KEY.strip()) == 0:
        raise ValueError("GROQ_API_KEY is empty or invalid. Please check your .env file.")
    
    # Try the primary model first
    models_to_try = [GROQ_MODEL] + [m for m in supported_models if m != GROQ_MODEL]
    
    last_error = None
    for model_name in models_to_try:
        try:
            result, error = await _call_groq_with_model(prompt, system_message, model_name)
            if result:
                if model_name != GROQ_MODEL:
                    print(f"Note: Used fallback model '{model_name}' instead of '{GROQ_MODEL}'")
                return result
            else:
                last_error = error
                # If it's a model decommissioned error, try next model
                if "decommissioned" in error.lower() or "model_decommissioned" in error.lower():
                    print(f"Model '{model_name}' is decommissioned, trying next model...")
                    continue
                # For other errors, still try next model but log it
                print(f"Error with model '{model_name}': {error}, trying next model...")
        except httpx.TimeoutException:
            raise Exception("Request to Groq API timed out. Please try again.")
        except httpx.RequestError as e:
            raise Exception(f"Error connecting to Groq API: {str(e)}")
        except Exception as e:
            last_error = str(e)
            print(f"Exception with model '{model_name}': {str(e)}, trying next model...")
            continue
    
    # If we get here, all models failed
    raise Exception(f"All models failed. Last error: {last_error}")
