from django.db import models

from apps.brands.models import BrandProfile

class Category(models.Model):
    
    name = models.CharField(max_length=300, blank=False, null=False)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.name 
    
class Product(models.Model):
    
    name = models.CharField(max_length=300, blank=False, null=False)
    
    seller = models.ForeignKey(
        BrandProfile, 
        on_delete=models.CASCADE,
        related_name='products'
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    
    description = models.TextField()
    
    price = models.DecimalField(max_digits=15, decimal_places=2)
    
    quantity = models.PositiveIntegerField(default=0, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.name} - {self.price}'
    