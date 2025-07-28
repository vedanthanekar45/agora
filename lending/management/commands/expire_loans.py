from lending.models import *
from django.http import JsonResponse
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

class Command (BaseCommand):
    
    def handle(self, *args, **kwargs):
        now = timezone.now()

        expired_loans = Loans.objects.filter(status='issued', return_date=now)
        if expired_loans.count() == 0:
            self.stdout.write(self.style.SUCCESS("No expired loans to process.."))

        for loan in expired_loans:
            loan.status = "returned"
            loan.save()
            self.stdout.write(self.style.WARNING(f'Loan ID {loan.id} has expired and was marked as returned.'))

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {expired_loans.count()} expired loans.'))