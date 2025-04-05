from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "category"
        verbose_name = "Categories"
        verbose_name_plural = "Categories"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"
    
    class Meta:
        db_table = "budget"
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    detail = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
    
    class Meta:
        db_table = "transactions"
        verbose_name = "Transaction Entry"
        verbose_name_plural = "Transactions"
        ordering = ['-date']
