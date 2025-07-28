from lending.models import *
from django.http import JsonResponse
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from library.models import *

class Command (BaseCommand):
    
    def handle(self, *args, **kwargs):
        now = timezone.now()

        expired_loans = Loans.objects.filter(status='issued', return_date=now)
        if expired_loans.count() == 0:
            self.stdout.write(self.style.SUCCESS("No expired loans to process.."))
            return

        for loan in expired_loans:
            book = loan.book
            loan.status = "returned"
            loan.save()
            self.stdout.write(self.style.WARNING(f'Loan ID {loan.id} has expired and was marked as returned.'))

            # <--- Waitlist logic here --->
            waitlist_entries = WaitlistModel.objects.filter(book=book).order_by('date added')

            if waitlist_entries.exists():
                next = waitlist_entries.first()
                next_patron = next.patron

                self.stdout.write(self.style.SUCCESS(
                    f'Notifying user "{next_patron.username}" that "{book.title}" is now available.'
                ))
                next.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {expired_loans.count()} expired loans.'))