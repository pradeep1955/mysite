"""
Seeds a 'Tools' category with a starter set of commonly-essential maker tools.

IMPORTANT: these are drafts, not a claim about what you actually own. Edit
name/spec/price/reason for each one in /admin/store/product/ to match your
real toolbench before publishing. Delete any you don't actually use — better
to have 4 real, honestly-reviewed tools than 10 generic placeholder ones.

Run:
    python manage.py seed_tools
"""
from django.core.management.base import BaseCommand

from store.models import Category, Product

CATEGORY_NAME = "Tools"
CATEGORY_ORDER = 5  # after Enclosure & Misc

# (name, specification, price_min, price_max, reason)
TOOLS = [
    ("Soldering iron", "Temperature-adjustable, 60-80W", 400, 1200,
     "EDIT ME: why this one, over a cheaper fixed-temp iron"),
    ("Digital multimeter", "Auto-ranging, continuity + diode test", 400, 1000,
     "EDIT ME: what you actually use it for most on these builds"),
    ("Wire stripper / cutter", "Adjustable for 10-24 AWG", 150, 400, ""),
    ("Breadboard", "830 tie-point, full size", 80, 150, ""),
    ("Jumper wire kit", "Male-male, male-female, female-female assortment", 100, 250, ""),
    ("Hot glue gun", "Mini size, for securing wiring/enclosures", 150, 350, ""),
    ("Precision screwdriver set", "For enclosures and small terminals", 200, 500, ""),
    ("Helping hands / PCB holder", "With magnifier, for soldering", 300, 700, ""),
]


class Command(BaseCommand):
    help = "Seeds a starter Tools category and placeholder products — EDIT before publishing."

    def handle(self, *args, **options):
        category, created = Category.objects.get_or_create(
            name=CATEGORY_NAME, defaults={"order": CATEGORY_ORDER}
        )
        self.stdout.write(f"{'Created' if created else 'Found'} category: {CATEGORY_NAME}")

        for name, spec, price_min, price_max, reason in TOOLS:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "specification": spec,
                    "price_min": price_min,
                    "price_max": price_max,
                    "reason": reason,
                    "is_active": False,  # off by default — flip on once you've reviewed/edited it
                },
            )
            self.stdout.write(f"{'Created' if created else 'Found'} tool: {name}")

        self.stdout.write(self.style.WARNING(
            "\nAll seeded tools are set is_active=False so nothing goes live by accident. "
            "Review each one in /admin/store/product/ — edit specs/price/reason to match "
            "what you actually use, delete what doesn't apply, then tick 'Active' to publish."
        ))