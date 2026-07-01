from django.db import models
from django.utils import timezone


class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("symbol", "date")
        ordering = ["-date"]
