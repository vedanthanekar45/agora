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


# View or method to return the borrowed asset

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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



# View to auto-return asset
def auto_close_loan (request):
    data = request.data

    loan_id = data.get('id')
    try:
        loan_data = Loans.objects.get(id=loan_id)
        if loan_data.return_date < datetime.now():
            loan_data.status = "returned"
            loan_data.save()

    except Loans.DoesNotExist:
        return JsonResponse({
            'message': "The body you're requesting for unfortunately doesn't exist."
        }, status=400)
    
    return JsonResponse({
        'message': "Asset successfully auto-returned."
    })