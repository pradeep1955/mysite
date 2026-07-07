from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Category, PreorderInterest, Product, ProjectKit


class StoreHomeView(ListView):
    """Landing page: every non-draft kit, plus categories for a quick parts browse."""
    model = ProjectKit
    template_name = "store/index.html"
    context_object_name = "kits"

    def get_queryset(self):
        return ProjectKit.objects.exclude(status=ProjectKit.STATUS_DRAFT)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        return ctx


class KitDetailView(DetailView):
    """Full kit page: story, BOM breakdown by category, price range, preorder form."""
    model = ProjectKit
    template_name = "store/kit_detail.html"
    context_object_name = "kit"

    def get_queryset(self):
        return ProjectKit.objects.exclude(status=ProjectKit.STATUS_DRAFT)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["components"] = (
            self.object.kitcomponent_set
            .select_related("product", "product__category")
        )
        return ctx


class ProductListView(ListView):
    """All individually-buyable components, filterable by category (?category=slug)."""
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"
    paginate_by = 24

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related("category")
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["active_category"] = self.request.GET.get("category", "")
        return ctx


class PreorderCreateView(View):
    """
    No payment gateway yet — just capture interest so you can follow up
    manually by WhatsApp/UPI once a kit has enough names on the list.
    """
    def post(self, request, slug):
        kit = get_object_or_404(ProjectKit, slug=slug)
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        if not name or not email:
            messages.error(request, "Please fill in at least your name and email.")
            return redirect("store:kit-detail", slug=slug)

        PreorderInterest.objects.create(
            kit=kit,
            name=name,
            email=email,
            phone=request.POST.get("phone", "").strip(),
            quantity=request.POST.get("quantity") or 1,
            message=request.POST.get("message", "").strip(),
        )
        messages.success(request, "Thanks — you're on the list. I'll reach out with next steps.")
        return redirect("store:kit-detail", slug=slug)
