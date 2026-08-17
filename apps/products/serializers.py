from rest_framework import serializers

from apps.brands.serializers import BrandProfileSerializer
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'name')
        
class ProductSerializer(serializers.ModelSerializer):
    
    seller = BrandProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product 
        fields = ('id', 'name', 'seller', 'category', 'description', 'price', 'quantity', 'created_at')
        read_only_fields = ['created_at']
        


        
    
    
    