import csv

from django.core.management.base import BaseCommand

from myapp.models import Contact


class Command(BaseCommand):
    help = "Export contacts to a CSV file on the server"

    def handle(self, *args, **kwargs):
        file_path = "data/list_updated.csv"
        contacts = Contact.objects.all()

        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["fname", "lname", "mobile", "Address", "Remark"])

            for contact in contacts:
                writer.writerow(
                    [
                        contact.fname,
                        contact.lname,
                        contact.mobile,
                        contact.Address,
                        contact.Remark,
                    ]
                )

        self.stdout.write(
            self.style.SUCCESS(f"Contacts exported successfully to {file_path}")
        )
