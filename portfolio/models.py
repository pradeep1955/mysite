from django.conf import settings
from django.db import models
from django.utils import timezone


class Holding(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ("user", "symbol")
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.user.username} - {self.quantity} shares of {self.symbol}"
