"""
Seeds the store with real content from the "Solar-Powered Automatic Drip
Irrigation System" project report, so the store launches with something
genuine instead of empty tables.

Run once with:
    python manage.py seed_solar_irrigation_kit

Safe to re-run — uses get_or_create/update_or_create throughout.
"""
from django.core.management.base import BaseCommand

from store.models import Category, KitComponent, Product, ProjectKit


# (category_name, order)
CATEGORIES = [
    ("Power & Charging", 1),
    ("Microcontroller & Control", 2),
    ("Water & Plumbing", 3),
    ("Enclosure & Misc", 4),
]

# (name, category, specification, price_min, price_max, kit_quantity, note)
# price_min/max is PER UNIT. Where the report gave a total for multiple units,
# it's been divided back down to a per-unit estimate.
PRODUCTS = [
    # Power & Charging
    ("Solar panel", "Power & Charging", "18V, 10-20W mono/poly", 600, 1200, 1, ""),
    ("CN3722 MPPT solar charge controller", "Power & Charging", "3S Li-ion, up to 2A", 300, 500, 1, ""),
    ("Schottky diode", "Power & Charging", "SR540 or SB540, 5A 40V", 20, 40, 1, "reverse current protection"),
    ("18650 Li-ion cell", "Power & Charging", "3000-3500mAh, matched batch, same brand/model", 135, 235, 3, ""),
    ("3S 18650 battery holder", "Power & Charging", "Plastic, with leads", 60, 100, 1, ""),
    ("HXYP-3S-B620 BMS", "Power & Charging", "3S, 20A, with balance wires", 150, 300, 1, "critical — see BMS balance wire notes"),
    ("XL4016 buck converter", "Power & Charging", "5A, adjustable, with display", 150, 250, 1, ""),
    ("Wirewound resistor", "Power & Charging", "3 ohm 5W (interim use)", 20, 40, 1, ""),

    # Microcontroller & Control
    ("ESP32-WROOM-32 dev board", "Microcontroller & Control", "30-pin, with USB", 350, 500, 1, ""),
    ("DS3231 RTC module", "Microcontroller & Control", "I2C, with CR2032 backup cell", 80, 150, 1, "prevents clock drift"),
    ("Single-channel relay module", "Microcontroller & Control", "5V coil, active LOW", 60, 100, 1, ""),
    ("Perfboard / veroboard", "Microcontroller & Control", "5cm x 7cm minimum", 30, 60, 1, ""),
    ("CR2032 coin cell", "Microcontroller & Control", "For DS3231 backup", 20, 40, 1, ""),
    ("Jumper wires / hookup wire", "Microcontroller & Control", "22 AWG, red/black/other", 50, 100, 1, ""),
    ("Screw terminals", "Microcontroller & Control", "2-pin, 3.5mm pitch", 7, 10, 4, ""),

    # Water & Plumbing
    ("Mini submersible DC pump", "Water & Plumbing", "5V or 12V, 60-120 LPH, 1-2m head", 150, 400, 1, ""),
    ("Water storage bucket", "Water & Plumbing", "15-20 litre, dark colour", 100, 200, 1, "dark colour prevents algae growth"),
    ("HDPE main pipe", "Water & Plumbing", "1/2 inch (16mm OD), ~3 metres", 80, 150, 1, ""),
    ("Micro feeder tube", "Water & Plumbing", "4mm OD, ~50cm each", 9, 15, 10, ""),
    ("Adjustable drip emitter", "Water & Plumbing", "2-4 LPH, barbed fitting", 10, 20, 10, ""),
    ("T-connector / tee joint", "Water & Plumbing", "16mm for main pipe", 10, 20, 5, ""),
    ("End cap", "Water & Plumbing", "16mm pipe end", 20, 30, 1, ""),
    ("Barbed connector", "Water & Plumbing", "16mm to 4mm", 6, 10, 10, ""),
    ("Pipe clamps / zip ties", "Water & Plumbing", "For wall/railing mounting", 40, 80, 1, ""),

    # Enclosure & Misc
    ("Weatherproof project box", "Enclosure & Misc", "~150mm x 100mm x 60mm", 150, 300, 1, "essential — Bengaluru monsoon"),
    ("Gland fitting / cable gland", "Enclosure & Misc", "PG7 size", 10, 20, 3, ""),
    ("Heat shrink tubing", "Enclosure & Misc", "Assorted sizes", 40, 80, 1, "use on all exposed solder joints near the battery"),
    ("3S cell voltage indicator", "Enclosure & Misc", "LED bar display, balance connector", 80, 150, 1, ""),
]

KIT_NAME = "Solar-Powered Balcony Drip Irrigation Kit"
KIT_TAGLINE = "Waters 8-10 pots on a fixed daily schedule — entirely off solar + battery."
KIT_SUMMARY = (
    "An ESP32 and DS3231 RTC fire a small submersible pump four times a day, "
    "watering 8-10 balcony flower pots through drip emitters. The whole system "
    "runs off a solar panel and a protected 3S Li-ion pack, so it needs no mains "
    "power at all."
)
KIT_FULL_DESCRIPTION = (
    "Built and tested on a front balcony in Bengaluru. The ESP32 keeps schedule "
    "via a DS3231 RTC (accurate even without Wi-Fi), switching a relay-driven "
    "pump on at 6am, 10am, 2pm and 6pm for 5 minutes each cycle — roughly "
    "8-14 litres a day across 10 pots. Power comes from an 18V solar panel "
    "through a CN3722 MPPT controller into a BMS-protected 3S 18650 pack, "
    "stepped down by an XL4016 buck converter. Full wiring notes, the BMS "
    "balance-wire gotcha, and the complete firmware are in the matching blog post."
)


class Command(BaseCommand):
    help = "Seeds Category, Product, and ProjectKit rows from the solar irrigation BOM."

    def handle(self, *args, **options):
        category_objs = {}
        for name, order in CATEGORIES:
            cat, created = Category.objects.get_or_create(name=name, defaults={"order": order})
            if not created and cat.order != order:
                cat.order = order
                cat.save(update_fields=["order"])
            category_objs[name] = cat
            self.stdout.write(f"{'Created' if created else 'Found'} category: {name}")

        kit, kit_created = ProjectKit.objects.get_or_create(
            name=KIT_NAME,
            defaults={
                "tagline": KIT_TAGLINE,
                "summary": KIT_SUMMARY,
                "full_description": KIT_FULL_DESCRIPTION,
                "status": ProjectKit.STATUS_COMING_SOON,
            },
        )
        self.stdout.write(f"{'Created' if kit_created else 'Found'} kit: {KIT_NAME}")

        for name, cat_name, spec, price_min, price_max, qty, note in PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category_objs[cat_name],
                    "specification": spec,
                    "price_min": price_min,
                    "price_max": price_max,
                },
            )
            KitComponent.objects.update_or_create(
                kit=kit,
                product=product,
                defaults={"quantity": qty, "note": note},
            )
            self.stdout.write(f"  {'Created' if created else 'Found'} product: {name}")

        low, high = kit.total_price_range
        self.stdout.write(self.style.SUCCESS(
            f"\nDone. '{KIT_NAME}' now has {kit.kitcomponent_set.count()} BOM line items, "
            f"estimated total ₹{low:,}-₹{high:,}."
        ))
        self.stdout.write(self.style.WARNING(
            "Kit status is 'coming_soon' by default — change it in /admin/ to 'preorder' when ready."
        ))
