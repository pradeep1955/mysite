from django.core.management.base import BaseCommand

from blog.utils import fetch_blog_from_url, post_blog_as_agent


class Command(BaseCommand):
    help = "Fetch news, generate blog with agent, and post as instructorHF"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            type=str,
            default="https://thehindu.com",
            help="News site URL to fetch content from",
        )

    def handle(self, *args, **options):
        url = options["url"]
        self.stdout.write(self.style.NOTICE(f"Fetching blog from {url}..."))

        blog_data = fetch_blog_from_url(url)
        title, content = blog_data["title"], blog_data["content"]

        post = post_blog_as_agent(title, content)

        self.stdout.write(
            self.style.SUCCESS(
                f"Blog posted successfully (ID={post.id}, Title='{title}')"
            )
        )
