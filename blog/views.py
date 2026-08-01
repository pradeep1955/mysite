from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Post

from datetime import datetime
from django.utils import timezone

import json
from django.utils.html import escapejs

cutoff = timezone.make_aware(datetime(2026, 7, 1))

def home(request):
    posts = Post.objects.filter(is_hidden=False).order_by("-date_posted")[:10]
    return render(request, "blog/home.html", {"posts": posts})


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_hidden=False).order_by("-date_posted")





class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


from django.http import Http404



class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.is_hidden and obj.author != self.request.user:
            raise Http404("Post not found")
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.object
        image_url = self.request.build_absolute_uri(post.image.url) if post.image else None
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": post.title,
            "description": post.seo_description,
            "datePublished": post.date_posted.isoformat(),
            "dateModified": post.date_posted.isoformat(),
            "author": {"@type": "Person", "name": post.author.get_full_name() or post.author.username},
            "publisher": {
                "@type": "Organization",
                "name": "TinkerStack",
                "url": self.request.build_absolute_uri("/"),
            },
            "mainEntityOfPage": self.request.build_absolute_uri(),
        }
        if image_url:
            schema["image"] = [image_url]
        # escape </script> so a stray substring in content can't break out of the tag
        ctx["ld_json"] = json.dumps(schema).replace("</", "<\\/")
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/blog/"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, "blog/about.html", {"title": "about"})
