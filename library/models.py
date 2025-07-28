from django.db import models

# The class Author is to create a ManyToMany Field in the books model.
# This is created because a single book can have multiple authors.

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# The books model is created to have a record of the books the library has. IF the library already uses LMS
# like Koha or FOLIO, their data may be referenced through an API. Smaller libraries with no LMS may use 
# this model.

class BooksModel (models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    ISBN = models.BigIntegerField()
    Publisher = models.CharField(max_length=255)
    no_of_copies = models.IntegerField(default=0)
    status = models.CharField(choices = [
        ("available", "Available"),
        ("checked_out", "Checked Out"),
        ("missing", "Missing"),
        ("damaged", "Damaged")
    ])
    additional_tags = models.CharField(default="N/A")

    def __str__ (self):
        return self.title



# Again a patron model for smaller libraries without any LMS

class PatronsModel (models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    books_lent = models.ManyToManyField(BooksModel)
    contact_number = models.BigIntegerField()


# Model for waitlist just in case the requested book doesn't exist

class WaitlistModel (models.Model):
    patron = models.ForeignKey(PatronsModel, on_delete=models.CASCADE)
    requested_book = models.ForeignKey(BooksModel, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('requested_book', 'patron')
        ordering = ['date_added']

    def __str__(self):
        return f"{self.patron.username} is waiting for {self.book.title}"

