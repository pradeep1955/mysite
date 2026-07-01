from django.db import models


class DailyNews(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)
    summary_html = models.TextField()

    def __str__(self):
        return f"News for {self.date}"
