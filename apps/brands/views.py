from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import BrandProfileRegisterSerializer, BrandProfileSerializer
from .models import BrandProfile

class BrandProfileRegisterView(CreateAPIView):
    queryset = BrandProfile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BrandProfileRegisterSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class BrandProfileDetailView(RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BrandProfileSerializer
    
    def get_queryset(self):
        return BrandProfile.objects.filter(user=self.request.user)
    
class BrandProfileListView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = BrandProfileSerializer
    
    def get_queryset(self):
        return BrandProfile.objects.filter(user=self.request.user)
    