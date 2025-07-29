from django.test import TestCase
from .models import *


# Test for the books and authors model
class TestLibrary (TestCase):

    def test_patron_creation (self):
        author = Author.objects.create(name="George R. R. Martin")
        book = BooksModel.objects.create(
            title="Fire and Blood",
            ISBN=9781524796280,
            Publisher="Bantam Books",
            no_of_copies=5,
            status="available"
        )
        book.authors.add(author)
        
        patron = PatronsModel.objects.create(
            full_name="Cassian Andor",
            email="cassianandor@gmail.com",
            contact_number= 403244993
        )
        patron.books_lent.add(book)