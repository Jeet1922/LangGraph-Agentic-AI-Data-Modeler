"""
Test script to check which Groq models are available.
Run this to find a working model for your API key.
"""
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# List of models to test
models_to_test = [
    "mixtral-8x7b-32768",
    "llama-3.2-11b-vision-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-90b-vision-preview",
    "gemma2-9b-it",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
]

async def test_model(model_name: str) -> bool:
    """Test if a model is available."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "Say 'test' if you can read this."}
        ],
        "temperature": 0.3,
        "max_tokens": 10
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(GROQ_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return True, None
            else:
                error_json = response.json()
                error_msg = error_json.get("error", {}).get("message", "Unknown error")
                return False, error_msg
    except Exception as e:
        return False, str(e)

async def main():
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY not set in environment variables!")
        return
    
    print("Testing Groq models...")
    print("=" * 60)
    
    working_models = []
    for model in models_to_test:
        print(f"Testing {model}...", end=" ")
        works, error = await test_model(model)
        if works:
            print("✅ WORKING")
            working_models.append(model)
        else:
            print(f"❌ FAILED: {error}")
    
    print("=" * 60)
    if working_models:
        print(f"\n✅ Working models: {', '.join(working_models)}")
        print(f"\nRecommended: Use '{working_models[0]}' as your default model")
        print(f"\nSet in .env file: GROQ_MODEL={working_models[0]}")
    else:
        print("\n❌ No working models found. Please check your API key.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

