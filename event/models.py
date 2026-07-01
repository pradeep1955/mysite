from django.db import models


class EventSchedule(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=60)

    def __str__(self):
        return f"{self.title} @ {self.venue}"


class Material(models.Model):
    event = models.ForeignKey(
        EventSchedule,
        on_delete=models.CASCADE,
        related_name="materials",
    )
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    is_arranged = models.BooleanField(default=False)
    remark = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"


class Task(models.Model):
    event = models.ForeignKey(
        EventSchedule,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    description = models.CharField(max_length=255)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.description} - {'Done' if self.is_completed else 'Pending'}"
