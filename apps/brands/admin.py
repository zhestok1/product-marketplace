from django.contrib import admin

from .models import BrandProfile, OOODetails, IPSEDetails

class OOODetailsInline(admin.TabularInline):
    model = OOODetails
    extra = 1
    
    
class IPSEDetailsInline(admin.TabularInline):
    model = IPSEDetails
    extra = 1
    
@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'brand_type', 'name', 'inn', 'ogrn' , 'created_at']
    list_filter = ['created_at', 'brand_type']
    readonly_fields = ['created_at']
    
    fieldsets = [
        ('Основная информация об организации', {'fields': ('user', 'brand_type', 
                                                           'name', 'inn', 
                                                           'ogrn' , 'created_at', )})
    ]
    
    add_fieldsets = [
        ('Основаная информация об организации', {
            'fields': ('user', 'brand_type', 'name', 'inn', 'ogrn', )
        })
    ]
    
    def get_inline_instances(self, request, obj = None):
        inline_instances = []
        
        if obj is not None:
            if obj.brand_type == 'OOO':
                inline_instances.append(OOODetailsInline(self.model, self.admin_site))
            else:
                inline_instances.append(IPSEDetails(self.model, self.admin_site))
                
        return inline_instances
            


