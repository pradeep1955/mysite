"""
Seeds a handful of starter Intents so the chat widget is useful on day one,
tied to Products already created by seed_solar_irrigation_kit.

Run:
    python manage.py seed_starter_intents

Run seed_solar_irrigation_kit FIRST — this looks up Products by name and
skips gracefully if a given product isn't found yet.
"""
from django.core.management.base import BaseCommand

from assistant.models import Intent
from store.models import Product


# (name, keywords, response, product_names)
INTENTS = [
    (
        "ESP32 vs Arduino",
        "esp32, arduino, which board, which microcontroller, what controller should i use",
        "For anything that needs Wi-Fi, a schedule, or room to grow later, I use "
        "an ESP32 — it's what's in every build on this site. A plain Arduino works "
        "too if you don't need Wi-Fi and want something even cheaper, but you'll "
        "outgrow it fast once you want scheduling or remote control.",
        ["ESP32-WROOM-32 dev board"],
    ),
    (
        "RTC / clock drift",
        "rtc, ds3231, clock drift, wrong time, schedule not accurate, timing off",
        "If your schedule slowly drifts or resets after a power cut, that's a "
        "clock problem, not a code problem — add a DS3231 RTC module. It keeps "
        "accurate time on its own tiny backup battery even when the ESP32 loses "
        "power or Wi-Fi.",
        ["DS3231 RTC module", "CR2032 coin cell"],
    ),
    (
        "Relay wiring / pump not switching",
        "relay, relay not working, pump not switching, relay chatter, active low, active high",
        "Most relay issues come down to two things: check whether your relay module "
        "is active-LOW or active-HIGH (flip the logic in code if it's backwards), "
        "and make sure the relay's power supply ground is tied back to the ESP32's "
        "ground — without a shared ground, switching gets unreliable.",
        ["Single-channel relay module"],
    ),
    (
        "Which pump to use",
        "pump, which pump, water pump, submersible pump, pump for irrigation, pump size",
        "For balcony-scale drip irrigation (8-10 pots), a small 5V or 12V "
        "submersible DC pump rated 60-120 LPH with a 1-2m head is plenty — no "
        "need to oversize it. Bigger pumps just drain your battery faster for no "
        "real benefit at this scale.",
        ["Mini submersible DC pump"],
    ),
    (
        "Solar / battery setup",
        "solar, battery, li-ion, bms, charging, solar panel, how to power without mains",
        "The solar builds here run an 18V panel through a CN3722 MPPT controller "
        "into a BMS-protected 3S 18650 pack, then step down with a buck converter. "
        "The BMS is non-negotiable — don't run Li-ion cells without one, and don't "
        "skip the balance wire connections or cell balancing won't work.",
        ["CN3722 MPPT solar charge controller", "HXYP-3S-B620 BMS", "18650 Li-ion cell"],
    ),
    (
        "Full irrigation kit",
        "irrigation kit, buy the whole thing, complete kit, all parts, whole build, drip irrigation kit",
        "The full parts list and prebuilt option for the balcony drip irrigation "
        "system is in the Solar-Powered Balcony Drip Irrigation Kit — one place "
        "with the whole BOM and pricing.",
        [],  # kit itself isn't a Product; response points them to the kit page
    ),
]


class Command(BaseCommand):
    help = "Seeds starter Intent entries for the chat widget."

    def handle(self, *args, **options):
        for name, keywords, response, product_names in INTENTS:
            intent, created = Intent.objects.get_or_create(
                name=name,
                defaults={"keywords": keywords, "response": response},
            )
            if not created:
                intent.keywords = keywords
                intent.response = response
                intent.save()

            products = Product.objects.filter(name__in=product_names)
            intent.products.set(products)

            missing = set(product_names) - set(products.values_list("name", flat=True))
            if missing:
                self.stdout.write(self.style.WARNING(
                    f"  '{name}': couldn't find product(s) {missing} — "
                    f"run seed_solar_irrigation_kit first, or check naming."
                ))

            self.stdout.write(f"{'Created' if created else 'Updated'} intent: {name}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. {len(INTENTS)} intents seeded."))