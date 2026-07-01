from django.shortcuts import render

from .utils import get_or_update_today_news


def show_news(request):
    news = get_or_update_today_news()
    return render(request, "news/news.html", {"news_summary": news.summary_html})
