from django.db import models
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Budget, Category, Transaction
from .serializers import BudgetSerializer, CategorySerializer, TransactionSerializer

class CategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TransactionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BudgetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = BudgetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_budget_status(self, request):
        """ Compare actual expenses vs. budget """
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        if not month or not year:
            return Response({"error": "Month and Year are required"}, status=status.HTTP_400_BAD_REQUEST)

        budget = Budget.objects.filter(user=request.user, month=month, year=year).first()
        if not budget:
            return Response({"message": "No budget set for this month"}, status=status.HTTP_404_NOT_FOUND)

        total_expenses = Transaction.objects.filter(
            user=request.user, 
            category__type="expense", 
            date__month=month, 
            date__year=year
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        return Response({
            "budget": budget.amount,
            "total_expenses": total_expenses,
            "remaining": float(budget.amount - total_expenses),
            "status": "Over Budget" if total_expenses > budget.amount else "Within Budget"
        })

