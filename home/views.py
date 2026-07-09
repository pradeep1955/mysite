from django.shortcuts import render
from django.views import View

from blog.models import Post

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
    
class PrivacyPolicyView(TemplateView):
    template_name = "home/privacy.html"    