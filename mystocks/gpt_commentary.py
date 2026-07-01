import os

from openai import OpenAI


def generate_gpt_comment(symbol, latest_rsi, latest_macd, latest_signal):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("default"):
        return "Missing or default API key. Please set it correctly."

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""You are a financial market expert. Based on these indicators for {symbol}:
- RSI: {latest_rsi}
- MACD: {latest_macd}
- Signal Line: {latest_signal}
Give a concise, human-like expert stock commentary: Buy, Sell, Hold advice and short reasoning.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            timeout=20,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error fetching AI commentary: {e}"
