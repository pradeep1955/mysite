from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(
            request,
            "home/main.html",
            {"site_name": "Pleasure Web Site", "message": "Minimal blog and home site ready for deployment."},
        )
