import os
from datetime import date

import feedparser
from django.conf import settings
from openai import OpenAI

from .models import DailyNews

# REMOVED: client = OpenAI()  ← was causing 401 on every test run

# SIMPLIFIED: now handled cleanly by python-decouple in settings.py
NEWS_API_KEY = settings.NEWS_API_KEY

def get_openai_client():
    """Lazy initialization — only connects to OpenAI when actually needed."""
    if not hasattr(get_openai_client, '_client'):
        get_openai_client._client = OpenAI()
    return get_openai_client._client

system_prompt = """
You are an expert Indian journalist.
"""

def create_user_prompt(articles):
    prompt_text = (
        "Here are today's top headlines from various Indian news sources. "
        "Please synthesize them into a summary:\n\n---\n\n"
    )
    for article in articles:
        prompt_text += f"Source: {article['source']}\n"
        prompt_text += f"Headline: {article['title']}\n"
        prompt_text += f"Description: {article.get('description', 'N/A')}\n\n"

    prompt_text += '''
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
        In summary, today's headlines highlight [main theme].
        The editorial emphasizes how these developments are interconnected.
    </p>
    </div>
    '''
    return prompt_text

def fetch_articles_from_rss(feed_urls):
    all_articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        source_name = feed.feed.title
        for entry in feed.entries:
            article = {
                "source": source_name,
                "title": entry.title,
                "description": (
                    entry.summary
                    if "summary" in entry
                    else "No description available."
                ),
                "link": entry.link,
            }
            all_articles.append(article)
    return all_articles

def get_or_update_today_news():
    today = date.today()
    try:
        return DailyNews.objects.get(date=today)
    except DailyNews.DoesNotExist:
        try:
            list_of_feeds = [
                "https://www.thehindu.com/feeder/default.rss",
                "http://rss.cnn.com/rss/edition.rss",
                "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
            ]

            articles_for_ai = fetch_articles_from_rss(list_of_feeds)
            if not articles_for_ai:
                raise ValueError("No articles could be fetched from RSS feeds.")

            user_prompt = create_user_prompt(articles_for_ai[:15])

            client = get_openai_client()        # ← lazy, only runs when actually needed
            ai_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            summary_html = ai_response.choices[0].message.content.strip()

            sources = {article["source"] for article in articles_for_ai[:15]}
            attribution_html = (
                '<p style="font-size: 0.8em; color: #555;"><em>Sources: '
                + ", ".join(sorted(list(sources)))
                + "</em></p>"
            )
            final_html = summary_html + attribution_html

            return DailyNews.objects.create(date=today, summary_html=final_html)

        except Exception as e:
            print(f"An error occurred while generating news from RSS: {e}")
            error_summary = (
                "<p>Today's news summary could not be generated at this time. "
                "Please check back later.</p>"
            )
            news, created = DailyNews.objects.get_or_create(
                date=today,
                defaults={"summary_html": error_summary},
            )
            return news