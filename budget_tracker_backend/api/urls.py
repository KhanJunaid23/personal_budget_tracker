from django.urls import path
from .views import (
    BudgetAPIView, 
    BudgetDetailAPIView, 
    BudgetSummaryAPIView, 
    CategoryAPIView, 
    CategoryDetailAPIView, 
    LoginView, 
    RefreshTokenView, 
    TransactionAPIView, 
    TransactionDetailAPIView, 
    TransactionSummaryAPIView
)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('transactions/', TransactionAPIView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),
    path('transactions/summary/', TransactionSummaryAPIView.as_view()),
    path('budgets/', BudgetAPIView.as_view(), name='budget-list'),
    path('budgets/<int:id>/', BudgetDetailAPIView.as_view(), name='budget-detail'),
    path('budgets/summary/', BudgetSummaryAPIView.as_view(), name='budget-summary'),
]