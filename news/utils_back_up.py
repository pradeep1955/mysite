import os
from datetime import date

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

from .models import DailyNews

env_path = os.path.expanduser("~/django_projects/mysite/.env")
load_dotenv(env_path, override=True)
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}


class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)


system_prompt = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that might be navigation related. "
    "Respond in html please do not mention the name of the website but "
    "mention To days news paper's abstract."
)


def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += (
        "\nThe contents of this website is as follows; "
        "please provide a short summary of the headlines and editorial "
        "of this website in html. "
        "Only include news and head line, then summarize.\n\n"
    )
    user_prompt += '''
Sample output is as under:
<div class="section">
    <h2 id="snap-insight" style="margin:0.5rem 0; letter-spacing:0.3px;">
    Snap Insight
    </h2>
    <p style="margin:0; font-size:0.95rem; opacity:0.8;">
    Quick takes on headlines & editorials
    </p>
    <ul style="font-family: Arial, sans-serif; font-size: clamp(1.5rem, 2.5vw, 2rem); line-height: 1.6;">
        <li>Headline 1 here</li>
        <li>Headline 2 here</li>
        <li>Headline 3 here</li>
    </ul>

    <h2>Editorial Summary</h2>
    <p style="font-family: Arial, sans-serif; font-size: 20px; line-height: 1.6;">
        In summary, today’s headlines highlight [main theme, e.g., “economic recovery, global trade, poltics, and technology growth”].
        The editorial emphasizes how these developments are interconnected, offering readers both the facts and the underlying context.
    </p>
</div>
'''

    user_prompt += website.text
    return user_prompt


def get_or_update_today_news():
    today = date.today()

    try:
        return DailyNews.objects.get(date=today)
    except DailyNews.DoesNotExist:
        thehindu = Website("https://thehindu.com")
        user_prompt = user_prompt_for(thehindu)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        summary = response.choices[0].message.content.strip()

        news = DailyNews.objects.create(date=today, summary_html=summary)
        return news
