from django.shortcuts import render
from django.views import View

from blog.models import Post

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Subscriber

from django.views.generic import TemplateView



class HomeView(View):
    def get(self, request):
        latest_post = Post.objects.order_by("-date_posted").first()
        return render(
            request,
            "home/main.html",
            {
                "site_name": "TinkerStack",
                "message": "Practical AI experiments, IoT builds, and electronics projects — with parts and kits coming soon.",
                "latest_post": latest_post,
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