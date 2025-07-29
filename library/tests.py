from django.test import TestCase
from .models import *


# Test for the books and authors model
class BookModelTest (TestCase):

    def test_book_creation (self):
        author = Author.objects.create(name="George R. R. Martin")

        book = BooksModel.objects.create(
            title="Fire and Blood",
            ISBN=9781524796280,
            Publisher="Bantam Books",
            no_of_copies=5,
            status="available"
        )
        book.authors.add(author)

        # saved_book = BooksModel.objects.get(id=book.id)
        # self.assertEqual(saved_book.title, 'Fire and Blood')