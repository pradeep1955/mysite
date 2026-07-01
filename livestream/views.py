from django.shortcuts import render

from .models import LiveStream


def live_stream(request):
    stream = LiveStream.objects.filter(is_live=True).first()
    return render(request, "livestream/live.html", {"stream": stream})
