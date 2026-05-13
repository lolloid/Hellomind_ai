import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

try:
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        timeout=10.0, # Add a timeout!
    )
    
    # Same prompt structure as main.py
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Halo, tes koneksi."}
    ]

    print("Sending request to Groq...", flush=True)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.6,
        top_p=0.9,
        max_tokens=200,
    )
    print("Response:")
    print(response.choices[0].message.content)
except Exception as e:
    import traceback
    traceback.print_exc()
