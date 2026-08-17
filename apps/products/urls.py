from django.urls import path
from .views import BrandProductCreateView, CategoryListView, CategoryView, ProductView

urlpatterns = [
    path('create/', BrandProductCreateView.as_view(), name='create'),
    path('catalog/', CategoryListView.as_view(), name='catalog'),
    path('category/<int:pk>/', CategoryView.as_view(), name='catefory_detail'),
    path('<int:pk>/', ProductView.as_view(), name='product_detail'),
]
