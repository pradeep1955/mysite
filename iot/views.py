from django.http import JsonResponse


def get_timer_config(request):
    data = {
        "red": 4,
        "green": 4,
        "blue": 4,
        "status": "run",
    }
    return JsonResponse(data)
