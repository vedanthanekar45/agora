from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import *
from library.models import *
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime   # <--- To handle dates and stuff

patron = get_user_model()
# This app will contain the core functionality, that are the lending mechanisms

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def make_loan (request):

    data = request.data
    book_id = data.get('book_id')

    try:
        book = BooksModel.objects.get(id=book_id)
    except BooksModel.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if book.no_of_copies == 0:
        return JsonResponse({'error': 'No copies available'}, status=400)

    existing_loan = Loans.objects.filter(book=book, patron=request.user)
    if existing_loan.status == "issued":
        return JsonResponse({'message': 'Loan already exists'}, status=400)


    loan_data = Loans.objects.get_or_create(
        book = book,
        patron = request.user,
        loan_period_in_days = data['loan_period_in_days'],
        issue_date = datetime.now(),
        return_date = datetime.now() + timedelta(days = 14),   # <--- The loan period for now is 14 days
        copies_available_after_loan = book.no_of_copies - 1,
    )

    if not loan_data:
        return JsonResponse({
            "message": "Loan already created!"
        }, status=400)

    return JsonResponse({
        'message': 'Loan made successfully'
    }, status=200)