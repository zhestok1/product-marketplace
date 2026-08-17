from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404

from apps.brands.models import BrandProfile
from .permissions import IsSellerWithBrand
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product

class BrandProductCreateView(CreateAPIView):
    permission_classes = [IsSellerWithBrand]
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        brand_id = self.kwargs.get('brand_id')
        brand = get_object_or_404(BrandProfile, pk=brand_id, user=self.request.user)
        serializer.save(seller=brand)
        
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    
class CategoryView(RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    
class ProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
