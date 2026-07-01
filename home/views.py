import json
import os
from datetime import timedelta

import openai
from dotenv import find_dotenv, load_dotenv
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from ads.models import Ad
from myapp.models import Video
from polls.models import Question

from .models import SensorReading
from news.utils import get_or_update_today_news

_ = load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]

sensor_data = {"temperature": None, "humidity": None}


@method_decorator(never_cache, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class HomeView(View):
    def get(self, request):
        today_news = get_or_update_today_news()

        now = timezone.now()
        start_time = now - timedelta(hours=12)
        readings = SensorReading.objects.filter(timestamp__gte=start_time).order_by(
            "timestamp"
        )

        interval_readings = []
        last_time = None
        for reading in readings:
            if not last_time or (reading.timestamp - last_time).total_seconds() >= 900:
                interval_readings.append(reading)
                last_time = reading.timestamp

        try:
            latest = SensorReading.objects.latest("timestamp")
        except SensorReading.DoesNotExist:
            latest = None

        latest_question = Question.objects.order_by("-pub_date").first()
        latest_video = Video.objects.filter(published=True).first()
        latest_ad = Ad.objects.order_by("-created_at").first()

        context = {
            "news_summary": today_news.summary_html,
            "temperature_data": [r.temperature for r in interval_readings],
            "humidity_data": [r.humidity for r in interval_readings],
            "labels": [
                localtime(r.timestamp).strftime("%H:%M") for r in interval_readings
            ],
            "temperature": latest.temperature if latest else None,
            "humidity": latest.humidity if latest else None,
            "last_updated": (
                localtime(latest.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                if latest
                else "No data"
            ),
            "latest_question": latest_question,
            "latest_video": latest_video,
            "latest_ad": latest_ad,
        }

        return render(request, "home/main.html", context)


@csrf_exempt
def receive_sensor_data(request):
    global sensor_data
    global corrected_data

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            temperature = data.get("temperature")
            humidity = data.get("humidity")
            sensor_data["temperature"] = temperature
            sensor_data["humidity"] = humidity

            SensorReading.objects.create(temperature=temperature, humidity=humidity)

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "only POST allowed"})


@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"message": "Please enter a valid message."})

            openai.api_key = settings.OPENAI_API_KEY

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": user_message},
                ],
            )

            chatbot_response = (
                response.choices[0].message.content
                if response.choices[0]
                else "No response from model."
            )

            return JsonResponse({"message": chatbot_response})

        except Exception as e:
            return JsonResponse(
                {
                    "message": (
                        "Error: Unable to process the request. "
                        f"Please try again. Detail: {e}"
                    )
                }
            )

    return JsonResponse({"message": "This endpoint only accepts POST requests."})
