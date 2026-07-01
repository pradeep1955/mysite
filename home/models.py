from django.db import models


class SensorReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.temperature}°C / {self.humidity}%"
