from django.core.management.base import BaseCommand

from apps.workload.services import WorkloadCalculationService


class Command(BaseCommand):
    help = 'Recalculates algorithmic workload scores for all active employees'

    def handle(self, *args, **options):
        self.stdout.write("Calculating employee workloads...")
        metrics = WorkloadCalculationService.recalculate_all_workloads()
        self.stdout.write(self.style.SUCCESS(f"Successfully calculated workloads for {len(metrics)} employees."))
