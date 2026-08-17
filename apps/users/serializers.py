from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style = {'input_style': 'password'},
    )
    
    password_confirm = serializers.CharField(
            write_only=True, 
            required=True, 
            validators=[validate_password],
            style = {'input_style': 'password'},
        )
    
    class Meta:
        model = User 
        fields = ('email', 'username', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True}
        }
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
             raise serializers.ValidationError({
                'password_confirm': 'Пароли не совпадают'
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        return user
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User 
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'balance')
        
        
class TopUpBalanceSerializer(serializers.Serializer):
    
    amount = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=True, 
        min_value=0.01,
    )
    
    def validate_amount(self, value):
        if value <= 0:
            return serializers.ValidationError("Сумма пополнения должна быть больше 0")
        
        return value
    
    