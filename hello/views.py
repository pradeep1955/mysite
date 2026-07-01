from django.http import HttpResponse


def myview(request):
    print(request.COOKIES)
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    if num_visits > 4:
        del request.session["num_visits"]

    response = HttpResponse(f"view count={num_visits}")
    response.set_cookie("dj4e_cookie", "2c600986", max_age=1000)
    return response
