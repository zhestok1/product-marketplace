from rest_framework import serializers

from .models import OOODetails, IPSEDetails, BrandProfile

class OOODetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OOODetails
        fields = ('id', 'brand', 'full_name', 'kpp', 'legal_address', )
        
        
class IPSEDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IPSEDetails
        fields = ('id', 'brand', 'first_name', 'last_name', 'passport_data',)
       
        
class BrandProfileRegisterSerializer(serializers.ModelSerializer):
    
    details = serializers.SerializerMethodField()

    class Meta:
        model = BrandProfile
        fields = ('id', 'user', 'brand_type', 'name', 'inn', 'ogrn', 'created_at', 'details')
        read_only_fields = ('created_at',)

    def get_details(self, obj):
        
        if obj.brand_type == 'OOO' and hasattr(obj, 'ooo_details'):
            return OOODetailsSerializer(obj.ooodetails).data
        elif obj.brand_type in ['IP', 'SE'] and hasattr(obj, 'ipse_details'):
            return IPSEDetailSerializer(obj.ipsedetails).data
        return None
    
class BrandProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
            model = BrandProfile
            fields = ('id', 'user', 'brand_type', 'name', 'inn', 'ogrn', 'created_at')
            read_only_fields = ('created_at',)