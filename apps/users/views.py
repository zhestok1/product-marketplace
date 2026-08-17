from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from decimal import Decimal, InvalidOperation

from django.contrib.auth import get_user_model

from .serializers import UserRegisterSerializer, UserSerializer
from .services import blacklist_refresh_token, top_up_balance

User = get_user_model()

class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    
class UserLoginView(TokenObtainPairView):
    pass 

class LogoutView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {
                    'error': 'refresh_token обязателен!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        answer = blacklist_refresh_token(refresh_token=refresh_token)
        
        if answer:
            return Response({
                'message': 'Логаут произошел успешно',
            },
               status=status.HTTP_205_RESET_CONTENT             
            )
            
        else:
            return Response({
                'error': 'Токен не действителен'
            }, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
class ProfileView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(
            instance=request.user,
            data=request.data,
            partial=True 
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
class TopUpBalanceView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(
            {
                'balance': str(request.user.balance)
            },
        )

    def post(self, request):
        amount_raw = request.data.get('amount')
        
        if amount_raw is None:
            return Response({
                'error': 'Вы не ввели сумму пополнения'
            }, 
                status=status.HTTP_400_BAD_REQUEST    
            )   
            
        try:
            amount = Decimal(str(amount_raw))

            new_balance = top_up_balance(request.user.balance, amount)
                    
            request.user.balance = new_balance
            request.user.save(update_fields=['balance'])
       
        
            return Response({
                'message': 'Вы успешно пополнили баланс',
                'balance': str(request.user.balance)
            }, 
                status=status.HTTP_200_OK
            )
            
        except (ValueError, TypeError, InvalidOperation):
            return Response(
                {
                    "error": "Сумма должна быть положительным числом",
                    
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    
    
    
        
        
    