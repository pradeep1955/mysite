import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from .models import ChatQuery, Intent

MATCH_THRESHOLD = 1  # at least 1 keyword hit required to count as a match

FALLBACK_RESPONSE = (
    "I don't have a canned answer for that one yet — but I've logged it, "
    "and it'll likely turn into a blog post. In the meantime, browse the "
    "parts catalog or check the latest build for something close."
)


@method_decorator(csrf_protect, name="dispatch")
class AskView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            payload = {}

        message = (payload.get("message") or request.POST.get("message") or "").strip()
        if not message:
            return JsonResponse({"error": "Empty message"}, status=400)

        message_lower = message.lower()

        best_intent = None
        best_score = 0
        for intent in Intent.objects.filter(is_active=True).prefetch_related("products"):
            score = intent.score(message_lower)
            if score > best_score or (score == best_score and score > 0 and intent.priority):
                if score > 0:
                    best_intent = intent
                    best_score = score

        matched = best_intent is not None and best_score >= MATCH_THRESHOLD

        ChatQuery.objects.create(
            question=message,
            matched_intent=best_intent if matched else None,
            matched=matched,
        )

        if matched:
            products = [
                {
                    "name": p.name,
                    "price": p.price_display,
                    "url": p.affiliate_url or None,
                }
                for p in best_intent.products.filter(is_active=True)
            ]
            return JsonResponse({
                "answer": best_intent.response,
                "products": products,
                "matched": True,
            })

        return JsonResponse({
            "answer": FALLBACK_RESPONSE,
            "products": [],
            "matched": False,
        })
