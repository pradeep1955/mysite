from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class OwnerListView(ListView):
    """List view base class."""


class OwnerDetailView(DetailView):
    """Detail view base class."""


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """Create view that sets owner to the logged-in user."""

    def form_valid(self, form):
        print("form_valid called")
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """Update view restricted to objects owned by the user."""

    def get_queryset(self):
        print("update get_queryset called")
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view restricted to objects owned by the user."""

    def get_queryset(self):
        print("delete get_queryset called")
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
