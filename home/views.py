from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(
            request,
            "home/main.html",
            {
                "site_name": "TinkerStack",
                "message": "Practical AI experiments, IoT builds, and electronics projects — with parts and kits coming soon.",
            },
        )
