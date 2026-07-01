import csv

from django.core.management.base import BaseCommand

from myapp.models import Contact


class Command(BaseCommand):
    help = "Import contacts from memory.csv file"

    def handle(self, *args, **kwargs):
        file_path = "data/list1.csv"
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                fname = row.get("fname", "").strip()
                lname = row.get("lname", "").strip()
                mobile = row.get("mobile", "").strip()
                address = row.get("Address", "").strip()
                remark = row.get("Remark", "").strip()

                if not fname or not lname:
                    self.stdout.write(
                        self.style.WARNING(f"Skipping row with missing name: {row}")
                    )
                    continue

                if mobile:
                    try:
                        contact, created = Contact.objects.get_or_create(
                            mobile=mobile,
                            defaults={
                                "fname": fname,
                                "lname": lname,
                                "Address": address,
                                "Remark": remark,
                            },
                        )
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Successfully imported contact: {fname} {lname}"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Contact with mobile {mobile} already exists."
                                )
                            )
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error importing row: {row}. Error: {str(e)}"
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Skipping row with missing mobile: {row}")
                    )

        self.stdout.write(self.style.SUCCESS("Import process completed"))
