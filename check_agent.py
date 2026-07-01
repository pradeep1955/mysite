"""
A minimal single-tool agent.

What this script teaches:
1. How to define a "tool" Claude can call (just a JSON schema description).
2. How to handle Claude's tool_use request (you run the actual code).
3. How to send the result back so Claude can finish answering.

Setup:
    pip install anthropic --break-system-packages
    export ANTHROPIC_API_KEY="your-key-here"

Run:
    python website_check_agent.py
"""

import requests
import time
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from environment

MODEL = "claude-sonnet-4-6"


# -----------------------------------------------------------------
# STEP 1: The actual Python function that does real work.
# This has nothing to do with AI -- it's a plain function.
# -----------------------------------------------------------------
def check_website_status(url: str) -> dict:
    """Pings a URL and returns its status code and response time."""
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = round(time.time() - start, 2)
        return {
            "url": url,
            "status_code": response.status_code,
            "is_up": response.status_code < 400,
            "response_time_seconds": elapsed,
        }
    except requests.RequestException as e:
        return {"url": url, "is_up": False, "error": str(e)}


# -----------------------------------------------------------------
# STEP 2: Describe that function to Claude as a "tool".
# Claude reads this description to decide WHEN to use it
# and WHAT input to provide. This is just a schema -- no code runs here.
# -----------------------------------------------------------------
tools = [
    {
        "name": "check_website_status",
        "description": (
            "Checks whether a website is reachable and returns its HTTP "
            "status code and response time. Use this whenever the user "
            "asks if a site is up, down, slow, or working."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL to check, e.g. https://example.com",
                }
            },
            "required": ["url"],
        },
    }
]

# Map tool name -> actual Python function to call
AVAILABLE_TOOLS = {
    "check_website_status": check_website_status,
}


# -----------------------------------------------------------------
# STEP 3: The agent loop.
# Send messages to Claude. If Claude asks for a tool, run it and
# send the result back. Repeat until Claude gives a final text answer.
# -----------------------------------------------------------------
def run_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        # Add Claude's response to the conversation history
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            # Claude wants to call one or more tools.
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    print(f"  [agent is calling tool: {tool_name}({tool_input})]")

                    func = AVAILABLE_TOOLS[tool_name]
                    result = func(**tool_input)

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        }
                    )

            # Send the tool results back to Claude as a new user turn
            messages.append({"role": "user", "content": tool_results})
            continue  # loop again so Claude can respond using the result

        # No more tool calls -- Claude has a final answer
        final_text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        return final_text


if __name__ == "__main__":
    question = input("Ask something (e.g. 'Is https://www.python.org up?'): ")
    answer = run_agent(question)
    print("\nClaude:", answer)
