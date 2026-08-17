from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class BrandProfile(models.Model):
    class BrandType(models.TextChoices):
        SELF_EMPLOYED = 'SE', 'Самозанятый'
        INDIVIDUAL_ENTREPRENEUR = 'IP', 'ИП'
        OOO = 'OOO', 'ООО'
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='brands'
    )
    brand_type = models.CharField(
        max_length=3,  
        choices=BrandType.choices,
    )

    name = models.CharField(max_length=255, verbose_name='Название бренда')
    inn = models.CharField(max_length=12, unique=True, verbose_name='ИНН')
    ogrn = models.CharField(max_length=15, blank=True, null=True, verbose_name='ОГРН/ОГРНИП')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_brand_type_display()} «{self.name}» (ИНН: {self.inn})"


class OOODetails(models.Model):
    brand = models.OneToOneField(
        BrandProfile, 
        on_delete=models.CASCADE, 
        related_name='ooo_details'
    )
    full_name = models.CharField(max_length=300, verbose_name='Полное наименование организации')
    kpp = models.CharField(max_length=9, verbose_name='КПП')
    legal_address = models.TextField(verbose_name='Юридический адрес')

    class Meta:
        verbose_name = 'Реквизиты ООО'
        verbose_name_plural = 'Реквизиты ООО'


class IPSEDetails(models.Model):  
    brand = models.OneToOneField(
        BrandProfile, 
        on_delete=models.CASCADE, 
        related_name='ipse_details'
    )
    first_name = models.CharField(max_length=300, verbose_name='Имя')
    last_name = models.CharField(max_length=300, verbose_name='Фамилия')
    
    passport_data = models.TextField(verbose_name='Паспортные данные')

    class Meta:
        verbose_name = 'Реквизиты ИП/Самозанятого'
        verbose_name_plural = 'Реквизиты ИП/Самозанятых'