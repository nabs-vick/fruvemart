from django.contrib import admin
from .models import Category, Customer,Order,Product,Feedback
from .models import Cart_components
# Register your models here.


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Feedback)




@admin.register(Cart_components)
class CartComponentsAdmin(admin.ModelAdmin):
    # Customize the list display
    list_display = ('name', 'product_name', 'price', 'user', 'phone_num', 'town', 'address', 'message')
    list_filter = ('user', 'product_name', 'town')  # Add filters for better navigation
    search_fields = ('name', 'product_name', 'user__username', 'town')  # Search functionality
