"""
Seeds Category, Product, and ProjectKit rows for the voice-controlled
LED counter project (ESP32-S3 + ESP-SR MultiNet + 5 LEDs).

Run:
    python manage.py seed_led_voice_counter_kit

Safe to re-run.
"""
from django.core.management.base import BaseCommand

from store.models import Category, KitComponent, Product, ProjectKit


AUDIO_CATEGORY = ("Audio & Voice I/O", 7)

# (name, category, specification, price_min, price_max, kit_quantity, note)
PRODUCTS = [
    ("ESP32-S3-WROOM-1 module", "Microcontroller & Control",
     "Bare module - needs the S3 variant specifically for AI acceleration instructions",
     300, 450, 1, "critical - must be S3, not plain ESP32"),
    ("Resistor 220-330 Ohm", "Microcontroller & Control",
     "LED current-limiting resistor", 2, 5, 5, ""),
    ("Jumper wires / hookup wire", "Microcontroller & Control",
     "22 AWG, red/black/other", 50, 100, 1, ""),

    ("I2S MEMS microphone module", "Audio & Voice I/O",
     "6-pin: V, G, WS, LR, CK, DA - LR ties to GND for single mono mic", 100, 200, 1,
     "LR pin sets channel - ground it for a single mic"),
    ("MAX98357A I2S amplifier", "Audio & Voice I/O",
     "I2S-in, speaker-out amplifier - no I2C, SD pin ties to 3.3V for always-on", 150, 300, 1, ""),
    ("Mini speaker", "Audio & Voice I/O",
     "0.25W, ~16 ohm", 30, 80, 1, ""),

    ("LED", "Enclosure & Misc", "5mm, any color", 5, 10, 5, ""),
    ("Breadboard", "Enclosure & Misc", "Full-size, for prototyping", 150, 300, 1, ""),
]

KIT_NAME = "Voice-Controlled LED Counter Kit"
KIT_TAGLINE = "Say a number, watch it count in light."
KIT_SUMMARY = (
    "An ESP32-S3 running Espressif's own MultiNet speech recognition, listening "
    "for a wake word then a spoken number one through five, lighting that many "
    "LEDs. Built entirely on custom breadboard hardware, with no reference board "
    "to fall back on."
)
KIT_FULL_DESCRIPTION = (
    "Uses ESP-SR (Espressif's speech recognition framework) with a custom board "
    "driver written from scratch, since this hardware combination isn't one of "
    "the officially supported reference boards. The I2S microphone and MAX98357A "
    "amplifier both speak raw I2S directly, with no codec chip in between, which "
    "kept the custom driver simpler than adapting a reference board's codec-based "
    "setup would have been. Recognition requires saying the wake word 'Hi, ESP' "
    "first, then a number within a 6-second window. Full build story - including "
    "a flash-size bug, a speech-model mismatch, and a one-line missing "
    "initialization call - is in the matching blog post."
)


class Command(BaseCommand):
    help = "Seeds Category, Product, and ProjectKit rows for the LED voice counter project."

    def handle(self, *args, **options):
        needed_categories = {"Microcontroller & Control", "Enclosure & Misc"}
        for name in needed_categories:
            cat, created = Category.objects.get_or_create(name=name, defaults={"order": 2})
            self.stdout.write(f"{'Created' if created else 'Found'} category: {name}")

        audio_name, audio_order = AUDIO_CATEGORY
        audio_cat, created = Category.objects.get_or_create(
            name=audio_name, defaults={"order": audio_order}
        )
        self.stdout.write(f"{'Created' if created else 'Found'} category: {audio_name}")

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
                kit=kit, product=product, defaults={"quantity": qty, "note": note},
            )
            self.stdout.write(f"  {'Created' if created else 'Found'} product: {name}")

        low, high = kit.total_price_range
        self.stdout.write(self.style.SUCCESS(
            f"\nDone. '{KIT_NAME}' has {kit.kitcomponent_set.count()} BOM items, "
            f"estimated total Rs.{low:,}-Rs.{high:,}."
        ))
