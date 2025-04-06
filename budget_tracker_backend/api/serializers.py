from rest_framework import serializers
from .models import Categories, Transaction, Budget

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'type']

class TransactionSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id', 
            'detail', 
            'amount', 
            'date', 
            'added_date', 
            'user', 
            'category',
            'category_id'
        ]
        read_only_fields = ['user', 'added_date', 'category']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
