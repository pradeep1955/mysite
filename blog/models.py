from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category-posts", kwargs={"slug": self.slug})



#class Post(models.Model):
#    title = models.CharField(max_length=100)
 #   content = models.TextField()
 #   date_posted = models.DateTimeField(default=timezone.now)
 #   author = models.ForeignKey(User, on_delete=models.CASCADE)
 #   image = models.ImageField(upload_to="blog/posts/", blank=True, null=True)
 #   meta_description = models.CharField(
 #       max_length=160, blank=True,
 #       help_text="SEO summary, 150-160 characters. Leave blank to auto-generate from content."
 #   )
 #   is_hidden = models.BooleanField(
 #       default=False,
 #       help_text="Hides this post from the public blog list and detail page. "
 #                  "Still visible to you in admin and when logged in as the author."
 #   )

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog/posts/", blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO summary, 150-160 characters.")
    categories = models.ManyToManyField(Category, blank=True, related_name="posts")
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    @property
    def seo_description(self):
        if self.meta_description:
            return self.meta_description
        text = " ".join(self.content.split())
        return (text[:157] + "…") if len(text) > 160 else text