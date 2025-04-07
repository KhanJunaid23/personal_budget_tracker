from datetime import date, datetime
from django.contrib.auth import authenticate
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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

    @swagger_auto_schema(
        operation_description="Authenticate user and get JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successfully authenticated",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Invalid credentials"
        }
    )
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
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Refresh JWT access token using refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="New access token",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            401: "Invalid or expired refresh token"
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            new_access = response.data.get('access')
            return Response({'access': new_access})
        return response
        
class CategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all categories for the authenticated user",
        responses={
            200: CategoriesSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def get(self, request):
        categories = Categories.objects.filter(user=request.user)
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new category",
        request_body=CategoriesSerializer,
        responses={
            201: CategoriesSerializer,
            400: "Bad request",
            401: "Unauthorized"
        }
    )
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

    @swagger_auto_schema(
        operation_description="Update a category",
        request_body=CategoriesSerializer,
        responses={
            200: CategoriesSerializer,
            400: "Bad request",
            401: "Unauthorized",
            404: "Category not found"
        }
    )
    def put(self, request, pk):
        category = self.get_object(pk, request.user)
        partial = request.method == 'PATCH'
        serializer = CategoriesSerializer(category, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a category",
        responses={
            204: "No content",
            401: "Unauthorized",
            404: "Category not found"
        }
    )
    def delete(self, request, pk):
        category = self.get_object(pk, request.user)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TransactionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List transactions with filters",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'startDate',
                openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'endDate',
                openapi.IN_QUERY,
                description="End date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'minAmount',
                openapi.IN_QUERY,
                description="Minimum amount",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'maxAmount',
                openapi.IN_QUERY,
                description="Maximum amount",
                type=openapi.TYPE_NUMBER
            ),
        ],
        responses={
            200: TransactionSerializer(many=True),
            401: "Unauthorized"
        }
    )
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

    @swagger_auto_schema(
        operation_description="Create a new transaction",
        request_body=TransactionSerializer,
        responses={
            201: TransactionSerializer,
            400: "Bad request",
            401: "Unauthorized"
        }
    )
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

    @swagger_auto_schema(
        operation_description="Retrieve a transaction",
        responses={
            200: TransactionSerializer,
            401: "Unauthorized",
            404: "Transaction not found"
        }
    )
    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a transaction",
        request_body=TransactionSerializer,
        responses={
            200: TransactionSerializer,
            400: "Bad request",
            401: "Unauthorized",
            404: "Transaction not found"
        }
    )
    def put(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a transaction",
        responses={
            204: "No content",
            401: "Unauthorized",
            404: "Transaction not found"
        }
    )
    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BudgetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all budgets for the authenticated user",
        responses={
            200: BudgetSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new budget",
        request_body=BudgetSerializer,
        responses={
            201: BudgetSerializer,
            400: "Bad request",
            401: "Unauthorized"
        }
    )
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

    @swagger_auto_schema(
        operation_description="Update a budget",
        request_body=BudgetSerializer,
        responses={
            200: BudgetSerializer,
            400: "Bad request",
            401: "Unauthorized",
            404: "Budget not found"
        }
    )
    def put(self, request, id):
        budget = self.get_object(id, request.user)
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a budget",
        responses={
            204: "No content",
            401: "Unauthorized",
            404: "Budget not found"
        }
    )
    def delete(self, request, id):
        budget = self.get_object(id, request.user)
        budget.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TransactionSummaryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get summary of transactions (income, expense, balance)",
        responses={
            200: openapi.Response(
                description="Transaction summary",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_income': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'total_expense': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'balance': openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                )
            ),
            401: "Unauthorized"
        }
    )
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

    @swagger_auto_schema(
        operation_description="Get budget summary for a specific month/year",
        manual_parameters=[
            openapi.Parameter(
                'month',
                openapi.IN_QUERY,
                description="Month (1-12)",
                type=openapi.TYPE_INTEGER,
                default=date.today().month
            ),
            openapi.Parameter(
                'year',
                openapi.IN_QUERY,
                description="Year",
                type=openapi.TYPE_INTEGER,
                default=date.today().year
            ),
        ],
        responses={
            200: openapi.Response(
                description="Budget summary",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'month': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'year': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'budget': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'actual_expense': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'remaining': openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                )
            ),
            401: "Unauthorized"
        }
    )
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
    
    

