from datetime import date, datetime
from django.contrib.auth import authenticate
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .models import Budget, Categories, Transaction
from .serializers import BudgetSerializer, CategoriesSerializer, TransactionSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response({'error': 'Invalid credentials'}, status=400)

class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            new_access = response.data.get('access')
            return Response({'access': new_access})
        return response
        
class CategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = Categories.objects.filter(user=request.user)
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = CategoriesSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Categories, pk=pk, user=user)

    def put(self, request, pk):
        category = self.get_object(pk, request.user)
        partial = request.method == 'PATCH'
        serializer = CategoriesSerializer(category, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk, request.user)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TransactionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).select_related('category')
        
        category_id = request.query_params.get('category')
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')
        min_amount = request.query_params.get('minAmount')
        max_amount = request.query_params.get('maxAmount')
        
        if category_id:
            transactions = transactions.filter(category_id=category_id)
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                transactions = transactions.filter(date__range=[start_date, end_date])
            except ValueError:
                pass
        
        if min_amount:
            try:
                transactions = transactions.filter(amount__gte=float(min_amount))
            except ValueError:
                pass
        if max_amount:
            try:
                transactions = transactions.filter(amount__lte=float(max_amount))
            except ValueError:
                pass
        transactions = transactions.order_by('-date')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TransactionDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Transaction, pk=pk, user=user)

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BudgetDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id, user):
        return get_object_or_404(Budget, id=id, user=user)

    def put(self, request, id):
        budget = self.get_object(id, request.user)
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        budget = self.get_object(id, request.user)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TransactionSummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        total_income = sum(t.amount for t in transactions if t.category.type == 'income')
        total_expense = sum(t.amount for t in transactions if t.category.type == 'expense')
        balance = total_income - total_expense
        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        })
    
class BudgetSummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        month = int(request.query_params.get("month", date.today().month))
        year = int(request.query_params.get("year", date.today().year))

        budget = Budget.objects.filter(user=user, month=month, year=year).first()
        budget_amount = budget.amount if budget else 0

        transactions = Transaction.objects.filter(
            user=user,
            date__month=month,
            date__year=year,
            category__type='expense'
        )

        total_expense = transactions.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            "month": month,
            "year": year,
            "budget": float(budget_amount),
            "actual_expense": float(total_expense),
            "remaining": float(budget_amount - total_expense)
        })
    
    

