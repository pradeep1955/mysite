from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from autos.models import Auto, Make


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        make_count = Make.objects.all().count()
        auto_list = Auto.objects.all()

        ctx = {"make_count": make_count, "auto_list": auto_list}
        return render(request, "autos/auto_list.html", ctx)


class MakeView(LoginRequiredMixin, View):
    def get(self, request):
        make_list = Make.objects.all()
        ctx = {"make_list": make_list}
        return render(request, "autos/make_list.html", ctx)


class MakeCreate(LoginRequiredMixin, CreateView):
    model = Make
    fields = "__all__"
    success_url = reverse_lazy("autos:all")


class MakeUpdate(LoginRequiredMixin, UpdateView):
    model = Make
    fields = "__all__"
    success_url = reverse_lazy("autos:all")


class MakeDelete(LoginRequiredMixin, View):
    model = Make
    fields = "__all__"
    success_url = reverse_lazy("autos:all")


class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    fields = "__all__"
    success_url = reverse_lazy("autos:all")


class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = "__all__"
    success_url = reverse_lazy("autos:all")


class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = "__all__"
    success_url = reverse_lazy("autos:all")
