from django.contrib import admin
from store.models import Category,Product,Cart,CartItem,Order,OrderItem
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','created','update']
    list_editable = ['price','stock']
    list_per_page = 10

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','name','email','total','token']
    list_per_page=5

class OrderItemAdmin(admin.ModelAdmin):
    list_display=['order','product','quantity','price']
    list_per_page=5

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)