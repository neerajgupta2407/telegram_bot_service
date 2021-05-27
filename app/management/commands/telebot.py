from django.core.management.base import BaseCommand
from apis.telegram_service.echobot import main

class Command(BaseCommand):
    help = "This is our telegram bot"

    def handle(self, *args, **options):
        main()
