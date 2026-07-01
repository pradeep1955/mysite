from django.db import models


class LiveStream(models.Model):
    title = models.CharField(max_length=100)
    is_live = models.BooleanField(default=False)
    playback_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
