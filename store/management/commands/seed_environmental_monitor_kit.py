"""
Seeds Category, Product, and ProjectKit rows from the Low-Power Environmental
Monitor project report (ESP8266 + MQ135 + DHT22 + OLED).

Run:
    python manage.py seed_environmental_monitor_kit

Safe to re-run — uses get_or_create/update_or_create throughout.
"""
from django.core.management.base import BaseCommand

from store.models import Category, KitComponent, Product, ProjectKit


# New category for this project — sensors/display, distinct from existing
# Microcontroller & Control / Power & Charging / Water & Plumbing / Enclosure & Misc
SENSOR_CATEGORY = ("Sensors & Display", 6)

# (name, category, specification, price_min, price_max, kit_quantity, note)
PRODUCTS = [
    ("NodeMCU ESP8266 dev board", "Microcontroller & Control",
     "Wi-Fi modem + microcontroller", 250, 400, 1, ""),
    ("2N2222 NPN transistor", "Microcontroller & Control",
     "TO-92 package — low-side switch for the MQ135 heater", 5, 15, 1,
     "critical — this is what makes battery operation possible"),
    ("Resistor 1kΩ", "Microcontroller & Control",
     "Transistor base trigger + voltage divider (used twice)", 2, 5, 2, ""),
    ("Resistor 2kΩ", "Microcontroller & Control",
     "Voltage divider, completes the ratio for the MQ135 analog line", 2, 5, 1, ""),
    ("Resistor 10kΩ", "Microcontroller & Control",
     "DHT22 data line pull-up — required, easy to forget", 2, 5, 1, ""),
    ("Prototype perfboard", "Microcontroller & Control",
     "For mounting the ESP8266 and wiring", 30, 60, 1, ""),

    ("MQ135 gas sensor module", "Sensors & Display",
     "Air quality — heater draws ~150mA, must be switched, not left on", 150, 300, 1,
     "power-hungry — this is why the transistor switch exists"),
    ("DHT22 temperature & humidity sensor", "Sensors & Display",
     "Needs a 10kOhm pull-up on the data line", 250, 450, 1, ""),
    ("0.96\" I2C OLED display", "Sensors & Display",
     "Local readout, I2C — SCL/SDA only", 200, 350, 1, ""),

    ("5V boost converter", "Power & Charging",
     "Steps up from the LiPo/18650 battery to power the MQ135 heater", 60, 120, 1, ""),
    ("LiPo / 18650 battery", "Power & Charging",
     "Main power source — deep sleep is what makes this last", 200, 400, 1, ""),
]

KIT_NAME = "Low-Power Environmental Monitor Kit"
KIT_TAGLINE = "Tracks temperature, humidity, and air quality — and sips power doing it."
KIT_SUMMARY = (
    "An ESP8266-based monitor that reads temperature, humidity, and air quality, "
    "shows readings on a local OLED, and reports over Wi-Fi — built around a "
    "transistor-switched gas sensor and deep sleep so it runs on battery for the "
    "long haul instead of needing constant power."
)
KIT_FULL_DESCRIPTION = (
    "The MQ135 gas sensor's heater draws power continuously if left on, which would "
    "drain a battery in hours. This build solves that with a 2N2222 transistor acting "
    "as a low-side switch on the sensor's ground line, controlled by the ESP8266 — "
    "the sensor only powers on for the ~1-2 minutes it needs to warm up and take a "
    "reading, then shuts off completely. Between readings, the ESP8266 itself drops "
    "into deep sleep (GPIO 16 wired to RST for the wake-up pulse), drawing only "
    "microamps. The MQ135's analog output needs a voltage divider (1k/2k resistors) "
    "before reaching the ESP8266's ADC, since it can output up to 5V and the ADC "
    "only tolerates 3.3V. Firmware (sensor timing, OLED rendering, HTTP reporting, "
    "sleep cycle management) is the next phase — full wiring notes are in the "
    "matching blog post."
)


class Command(BaseCommand):
    help = "Seeds Category, Product, and ProjectKit rows for the environmental monitor project."

    def handle(self, *args, **options):
        # Ensure all needed categories exist (reuses existing ones where possible)
        needed_categories = {"Microcontroller & Control", "Power & Charging"}
        for name in needed_categories:
            cat, created = Category.objects.get_or_create(name=name, defaults={"order": 2})
            self.stdout.write(f"{'Created' if created else 'Found'} category: {name}")

        sensor_name, sensor_order = SENSOR_CATEGORY
        sensor_cat, created = Category.objects.get_or_create(
            name=sensor_name, defaults={"order": sensor_order}
        )
        self.stdout.write(f"{'Created' if created else 'Found'} category: {sensor_name}")

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
            category = Category.objects.get(name=cat_name)
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
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
            "Kit status is 'coming_soon' — firmware isn't finished per the project report. "
            "Consider leaving it at coming_soon (or switching to 'draft' to hide it from the "
            "public store entirely) until the firmware/full working system is done."
        ))