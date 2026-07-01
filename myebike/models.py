from django.db import models


class Ride(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride {self.id}: {self.name}"


class GpsLog(models.Model):
    ride = models.ForeignKey(
        Ride,
        related_name="logs",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField(default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.ride.name} @ {self.timestamp.strftime('%H:%M')}"
