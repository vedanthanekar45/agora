from django.db import models
from library.models import BooksModel, PatronsModel

# The Loans model will be for everyone as it is the core functionality of the application.

class Loans (models.Model):
    book = models.ForeignKey(BooksModel, on_delete=models.CASCADE)
    patron = models.ForeignKey(PatronsModel, on_delete=models.CASCADE)

    # Default loan period can be set by the user while setting up the lending infrastructure.
    loan_period_in_days = models.IntegerField(default=7)
    issue_date = models.DateTimeField()
    return_date = models.DateTimeField()
    copies_available_after_loan = models.IntegerField()
    readium_link = models.URLField()
    status = models.CharField(choices= [
        ("issued", "Issued"),
        ("returned", "Returned")
    ], default="issued")