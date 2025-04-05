from django.urls import path
from .views import CategoryAPIView, CategoryDetailAPIView, LoginView, LogoutView, TransactionAPIView, TransactionDetailAPIView, TransactionSummaryAPIView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('transactions/', TransactionAPIView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),
    path('transactions/summary/', TransactionSummaryAPIView.as_view()),
]