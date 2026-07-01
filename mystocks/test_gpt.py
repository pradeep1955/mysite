import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai.api_key)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Give me a one-line stock market tip."}],
        temperature=0.5,
        timeout=20,
    )
    print(response.choices[0].message.content.strip())
except Exception as e:
    print(f"Error: {e}")
