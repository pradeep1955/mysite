import json

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from blog.models import Post

from .models import SensorReading, Subscriber



class HomeView(View):
    def get(self, request):
        latest_post = Post.objects.order_by("-date_posted").first()
        latest_sensor = SensorReading.objects.order_by("-timestamp").first()
        return render(
            request,
            "home/main.html",
            {
                "site_name": "TinkerStack",
                "message": "Practical AI experiments, IoT builds, and electronics projects — with parts and kits coming soon.",
                "latest_post": latest_post,
                "latest_sensor": latest_sensor,
            },
        )
    



class SubscribeView(View):
    def post(self, request):
        email = request.POST.get("email", "").strip()
        source = request.POST.get("source", "").strip()
        next_url = request.POST.get("next") or "/"

        if not email:
            messages.error(request, "Please enter an email address.")
            return redirect(next_url)

        _, created = Subscriber.objects.get_or_create(email=email, defaults={"source": source})
        if created:
            messages.success(request, "You're in — I'll email you when something new ships.")
        else:
            messages.success(request, "You're already on the list!")

        return redirect(next_url)

class PrivacyPolicyView(TemplateView):
    template_name = "home/privacy.html"    


@csrf_exempt
@require_http_methods(["GET", "POST"])
def sensor_data_api(request):
    if request.method == "GET":
        latest_sensor = SensorReading.objects.order_by("-timestamp").first()
        if latest_sensor is None:
            return JsonResponse({"status": "empty", "message": "No sensor readings yet."})

        return JsonResponse(
            {
                "status": "ok",
                "temperature": latest_sensor.temperature,
                "humidity": latest_sensor.humidity,
                "air_quality": latest_sensor.air_quality,
                "timestamp": latest_sensor.timestamp.isoformat(),
            }
        )

    expected_key = getattr(settings, "SENSOR_API_KEY", "")
    provided_key = request.headers.get("X-API-Key") or request.POST.get("api_key")

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)

    provided_key = provided_key or payload.get("api_key")
    if expected_key and provided_key != expected_key:
        return JsonResponse({"status": "error", "message": "Invalid API key."}, status=403)

    try:
        temperature = float(payload["temperature"])
        humidity = float(payload["humidity"])
        air_quality = int(payload["air_quality"])
    except (KeyError, TypeError, ValueError):
        return JsonResponse(
            {
                "status": "error",
                "message": "Send numeric temperature, humidity, and air_quality values.",
            },
            status=400,
        )

    reading = SensorReading.objects.create(
        temperature=temperature,
        humidity=humidity,
        air_quality=air_quality,
    )

    return JsonResponse(
        {
            "status": "ok",
            "id": reading.pk,
            "timestamp": reading.timestamp.isoformat(),
        },
        status=201,
    )
