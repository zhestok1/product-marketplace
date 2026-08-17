from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from decimal import Decimal

def blacklist_refresh_token(refresh_token):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True
    except TokenError:
        return False 
    
def top_up_balance(balance, amount):
    
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))
        
    if amount <= 0:
        raise ValueError('Сумма пополнения должна быть больше нуля')
        
    return balance + amount
        
    
    