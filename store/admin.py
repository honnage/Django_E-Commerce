from django.contrib import admin
from store.models import Category,Product,Cart,CartItem
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','created','update']
    list_editable = ['price','stock']
    list_per_page = 10

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
