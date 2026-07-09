from django.db import models

from store.models import Product

import re


class Intent(models.Model):
    """
    One 'thing people might ask about'. Matching is pure keyword scoring —
    no LLM call, no API cost, works fine on a free PythonAnywhere plan.

    Example:
        name: "ESP32 vs Arduino"
        keywords: "esp32, arduino, which board, which microcontroller"
        response: "For anything with Wi-Fi or a schedule to keep, I use an
                   ESP32 — it's what's in all the builds on this site..."
        products: [ESP32-WROOM-32 dev board]
    """
    name = models.CharField(max_length=150, help_text="Internal label, not shown to visitors")
    keywords = models.TextField(
        help_text="Comma-separated. Include how people actually phrase it, "
                   "not just the product name — e.g. 'pump not working, pump silent, no water'"
    )
    response = models.TextField(help_text="The canned answer shown to the visitor")
    products = models.ManyToManyField(
        Product, blank=True, related_name="intents",
        help_text="Products to surface (with Buy links) alongside this answer"
    )
    priority = models.PositiveIntegerField(
        default=0, help_text="Higher priority wins on a tied keyword score"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-priority", "name"]

    def __str__(self):
        return self.name

    def keyword_list(self):
        return [k.strip().lower() for k in self.keywords.split(",") if k.strip()]

    def score(self, message_lower):
        """Count keyword hits, matched as whole words/phrases, not substrings."""
        score = 0
        for kw in self.keyword_list():
            if re.search(r'\b' + re.escape(kw) + r'\b', message_lower):
                score += 1
        return score


class ChatQuery(models.Model):
    """
    Every question asked, whether or not it matched anything. The unmatched
    ones are the useful ones — they're free research into what to write your
    next blog post or FAQ about.
    """
    question = models.TextField()
    matched_intent = models.ForeignKey(
        Intent, null=True, blank=True, on_delete=models.SET_NULL, related_name="queries"
    )
    matched = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Chat queries"

    def __str__(self):
        return self.question[:60]
