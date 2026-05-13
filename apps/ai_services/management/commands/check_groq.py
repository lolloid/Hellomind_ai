import json

from django.core.management.base import BaseCommand, CommandError

from apps.ai_services.services import check_groq_connection


class Command(BaseCommand):
    help = "Check Groq API connectivity, model, and API key status without exposing secrets."

    def handle(self, *args, **options):
        result = check_groq_connection()
        self.stdout.write(json.dumps(result, indent=2, ensure_ascii=False))
        if not result["ok"]:
            raise CommandError(result["message"])
