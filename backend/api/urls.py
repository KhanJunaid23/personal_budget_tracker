from django.urls import path
from .views import CategoryAPIView, TransactionAPIView, BudgetAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('transactions/', TransactionAPIView.as_view(), name='transactions'),
    path('budget/', BudgetAPIView.as_view(), name='budget'),
]
