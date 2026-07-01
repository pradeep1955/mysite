import json
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db import close_old_connections
from django.utils import timezone
from openai import OpenAI
from .models import Post

# REMOVED: openai = OpenAI()  ← was causing 401 on every test run

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

def get_openai_client():
    """Lazy initialization — only connects to OpenAI when actually needed."""
    if not hasattr(get_openai_client, '_client'):
        get_openai_client._client = OpenAI()
    return get_openai_client._client

class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

system_prompt = """
You are a professional blogger.
From the provided newspaper content, write a blog in the following strict JSON format only:
{
  "title": "A short, catchy blog title",
  "content": "The full blog post content with introduction, summary, context, and conclusion."
}
Rules:
- Title must be concise (max 12 words).
- Content should be conversational but professional.
- Do not mention the name of the source website.
"""

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": website.text},
    ]

def fetch_blog_from_url(url):
    client = get_openai_client()        # ← gets client only when this function is called
    website = Website(url)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(website),
    )
    raw = response.choices[0].message.content.strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("JSON parse failed. Raw output:\n", raw)
        data = {"title": "Untitled Blog", "content": raw}
    return data

def post_blog_as_agent(title, content, username="instructorHF"):
    close_old_connections()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist as exc:
        raise ValueError(f"User {username} does not exist") from exc
    post = Post.objects.create(
        author=user,
        title=title,
        content=content,
        date_posted=timezone.now(),
    )
    return post