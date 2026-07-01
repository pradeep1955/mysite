from datetime import date

from django.core.management.base import BaseCommand

from news.models import DailyNews
from news.utils import fetch_news_html


class Command(BaseCommand):
    help = "Fetch and update news at 6 AM daily"

    def handle(self, *args, **kwargs):
        today = date.today()
        if not DailyNews.objects.filter(date=today).exists():
            summary = fetch_news_html()
            DailyNews.objects.create(html_summary=summary)
            self.stdout.write("News fetched successfully.")
        else:
            self.stdout.write("News already exists.")
