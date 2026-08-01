from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog/posts/", blank=True, null=True)
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text="SEO summary, 150-160 characters. Leave blank to auto-generate from content."
    )
    is_hidden = models.BooleanField(
        default=False,
        help_text="Hides this post from the public blog list and detail page. "
                   "Still visible to you in admin and when logged in as the author."
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    @property
    def seo_description(self):
        if self.meta_description:
            return self.meta_description
        # strip newlines, collapse whitespace, then truncate cleanly
        text = " ".join(self.content.split())
        return (text[:157] + "…") if len(text) > 160 else text