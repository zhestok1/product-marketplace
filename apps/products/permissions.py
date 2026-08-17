from rest_framework.permissions import BasePermission

class IsSellerWithBrand(BasePermission):
    message = "У вас должен быть зарегистрированный бренд, чтобы создавать товары."
    
    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.brands.exists()
            