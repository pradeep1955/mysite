from django.core.management.base import BaseCommand

from polls.utils import generate_and_save_daily_poll


class Command(BaseCommand):
    help = "Generates and saves a new poll question using the OpenAI API"

    def handle(self, *args, **kwargs):
        self.stdout.write("Attempting to generate a new poll...")
        new_poll = generate_and_save_daily_poll()
        if new_poll:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created poll: "{new_poll.question_text}"'
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR("Failed to create a new poll. Check the logs for details.")
            )
