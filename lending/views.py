from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import *
from library.models import *

from datetime import timedelta, datetime   # <--- To handle dates and stuff

patron = get_user_model()
# This app will contain the core functionality, that are the lending mechanisms

@api_view(['POST'])
def make_loan (request):

    data = request.data
    book_id = data.get('book_id')

    try:
        book = BooksModel.objects.get(id=book_id)
    except BooksModel.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if book.no_of_copies == 0:
        return JsonResponse({'error': 'No copies available'}, status=400)

    if Loans.objects.filter(book=book, patron=request.user, status="issued").exists():
        return JsonResponse({'message': 'Loan already exists'}, status=400)

    loan_data, created = Loans.objects.get_or_create(
        book = book,
        patron = request.user,
        loan_period_in_days = data['loan_period_in_days'],
        issue_date = datetime.now(),
        return_date = datetime.now() + timedelta(days = 14),   # <--- The loan period for now is 14 days
        copies_available_after_loan = book.no_of_copies - 1,
    )

    if not created:
        return JsonResponse({
            "message": "Loan already created!"
        }, status=400)
    
    book.no_of_copies -= 1
    book.save()

    return JsonResponse({
        'message': 'Loan made successfully'
    }, status=200)


# View or method to return the borrowed asset

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def close_loan (request):
    data = request.data

    loan_id = data.get('id')
    try:
        loan_data = Loans.objects.get(id=loan_id)
        loan_data.status = "returned"
        loan_data.save()

    except Loans.DoesNotExist:
        return JsonResponse({
            'message': "The body you're requesting for unfortunately doesn't exist."
        }, status=400)
    
    return JsonResponse({
        'message': "Asset successfully returned."
    })


# A waitlist will be created if the requested book is not available for the user

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def join_waitlist(request, book_id):
    book = get_object_or_404(BooksModel, id=book_id)
    patron = request.user

    has_loan = Loans.objects.filter(patron=patron, book=book, status='issued')
    if has_loan:
        messages.error(request, "You already have this book on loan.")
        return redirect('book_detail', pk=book_id)
    
    is_on_waitlist = WaitlistModel.objects.filter(patron=patron, book=book).exists()
    if is_on_waitlist:
        messages.warning(request, "You are already on the waitlist for this book.")
        return redirect('book_detail', pk=book_id)

    WaitlistModel.objects.create(book=book, patron=patron)
    messages.success(request, f"You have been added to the waitlist for '{book.title}'.")
    
    return redirect('book_detail', pk=book_id)