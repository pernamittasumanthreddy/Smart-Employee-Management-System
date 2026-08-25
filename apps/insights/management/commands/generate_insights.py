from django.core.management.base import BaseCommand

from apps.insights.insight_service import SmartInsightService


class Command(BaseCommand):
    help = 'Triggers full local machine learning and statistical smart insights analysis'

    def handle(self, *args, **options):
        self.stdout.write("Running local Smart Insights ML and statistical engine...")
        count = SmartInsightService.run_full_system_analysis()
        self.stdout.write(self.style.SUCCESS(f"Successfully generated {count} explainable actionable smart insights."))
