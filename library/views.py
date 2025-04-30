from django.http import JsonResponse
from .models import *
from rest_framework.decorators import api_view
# from dotenv import load_dotenv
# from os import getenv
# import requests

# This app will usually consist functionalities that small libraries that don't have a digital Library
# Management sytem will work on.
# Libraries with a working Library Management System won't have to enter their data manually into this 
# lending system, and instead will be able to import directly through their LMS like Koha, FOLIO, etc.
# Though I am originally planning to help them import through an Excel file or a CSV file.

# I am planning to have the features to manage book and patron data manually through APIs just as to build
# a Minimum Viable Product, though I'm planning to keep them in the final build.



# API View to add a book record. Admin will add to add each of them manually.
@api_view(['POST'])
def add_book (request):
    data = request.data

    bookData = BooksModel.objects.get_or_create(
        title = data['title'],
        authors = data['authors'],
        ISBN = data['ISBN'],
        Publisher = data['publisher'],
        status = data['status'],
        additional_tags = data['tags'],
    )

    if not bookData:
        return JsonResponse({
            'message': 'There has been an error creating that record!'
        }, status=400)
    
    return JsonResponse({
        'message': 'Record created successfully!'
    }, bookData, status=200)



# API View to add a Patron record.
@api_view(['POST'])
def add_patron (request):
    data = request.data

    patronData = PatronsModel.objects.get_or_create(
        full_name = data['full_name'],
        email = data['email'],
        book_lent = data['books_lent'],
        contact_number = data['contact']
    )

    if not patronData:
        return JsonResponse({
            'message': 'There has been an error creating that record!'
        }, status=400)
    
    return JsonResponse({
        'message': 'Record created successfully!'
    }, patronData, status=200)