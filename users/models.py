from io import BytesIO

from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="myapp/images/default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            if not self.image:
                return

            self.image.open()
            img = Image.open(self.image)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)

                thumb_io = BytesIO()
                image_format = "PNG" if img.mode == "RGBA" else "JPEG"
                img.save(thumb_io, format=image_format, quality=95)
                thumb_io.seek(0)

                self.image.save(self.image.name, File(thumb_io), save=False)
                super().save(update_fields=["image"])

        except FileNotFoundError:
            print(
                f"Warning: Could not find file {self.image.name} in S3 for "
                f"user {self.user.username}. Skipping image processing."
            )
            pass
