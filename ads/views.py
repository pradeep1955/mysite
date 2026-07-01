from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ads.forms import CommentForm, CreateForm
from ads.models import Ad, Comment, Fav
from ads.owner import OwnerDeleteView, OwnerDetailView, OwnerListView


class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"

    def get(self, request):
        strval = request.GET.get("search", False)
        if strval:
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().order_by("-updated_at")[:10]
        else:
            ad_list = Ad.objects.all().order_by("-updated_at")[:10]

        for obj in ad_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {"ad_list": ad_list, "search": strval}
        return render(request, self.template_name, ctx)


class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"

    def get(self, request, pk):
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by("-updated_at")
        comment_form = CommentForm()
        context = {"ad": ad, "comments": comments, "comment_form": comment_form}
        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin, View):
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:all")

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {"form": form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        form.save_m2m()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:all")

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {"form": form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {"form": form}
            return render(request, self.template_name, ctx)

        form.save()
        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = "ads/ad_confirm_delete.html"
    success_url = reverse_lazy("ads:all")


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response["Content-Type"] = ad.content_type
    response["Content-Length"] = len(ad.picture)
    response.write(ad.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.ad = ad
            comment.owner = request.user
            comment.save()
            return redirect(reverse("ads:ad_detail", args=[pk]))

        return redirect(reverse("ads:ad_detail", args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    def get_success_url(self):
        ad = self.object.ad
        return reverse("ads:ad_detail", args=[ad.id])


@method_decorator(csrf_exempt, name="dispatch")
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Add PK", pk)
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=ad)
        try:
            fav.save()
        except IntegrityError:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print("Delete PK", pk)
        ad = get_object_or_404(Ad, id=pk)
        try:
            Fav.objects.get(user=request.user, ad=ad).delete()
        except Fav.DoesNotExist:
            pass

        return HttpResponse()
