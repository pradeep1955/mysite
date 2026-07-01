from django.core.management.base import BaseCommand

from mystocks.utils import save_stock_data


class Command(BaseCommand):
    help = "Fetch and store SBIN.BO stock data"

    def handle(self, *args, **kwargs):
        save_stock_data()
        self.stdout.write(self.style.SUCCESS("Stock data updated."))
