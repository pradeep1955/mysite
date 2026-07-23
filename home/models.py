from django.db import models


class SensorReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    air_quality = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.timestamp}: {self.temperature}°C / "
            f"{self.humidity}% / AQ {self.air_quality}"
        )

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    source = models.CharField(
        max_length=50, blank=True,
        help_text="Where they signed up — e.g. 'homepage', 'blog'"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
