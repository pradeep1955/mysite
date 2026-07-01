from django.db import models
from django.utils import timezone


class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    Address = models.TextField()
    Remark = models.TextField()
    invited = models.BooleanField(default=False)

    arrival_date = models.DateField(null=True, blank=True)
    mode_arrival = models.CharField(max_length=100, null=True, blank=True)
    arrival_ref = models.CharField(max_length=100, null=True, blank=True)
    room_no = models.CharField(max_length=10, null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    departure_ref = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    tariff = models.IntegerField()

    def __str__(self):
        return self.name


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} at {self.visit_time.strftime('%Y-%m-%d %H:%M:%S')}"


class DailyMessage(models.Model):
    message_text = models.TextField(
        help_text="Type your daily greeting here. It will be used for all contacts."
    )
    message_image = models.ImageField(
        upload_to="daily_images/",
        null=True,
        blank=True,
        help_text="Upload the image you created in GIMP.",
    )
    created_date = models.DateField(
        default=timezone.now,
        unique=True,
        help_text="The date this message is for.",
    )

    def __str__(self):
        return f"Message for {self.created_date.strftime('%Y-%m-%d')}"


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to="videos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-uploaded_at"]
