from django.urls import path 

from .views import BrandProfileListView, BrandProfileRegisterView, BrandProfileDetailView

urlpatterns = [
    path('brands/', BrandProfileListView.as_view(), name='brand_list'),
    path('<int:pk>/', BrandProfileDetailView.as_view(), name='brand'),
    path('register/', BrandProfileRegisterView.as_view(), name='brand_register'),
]
