from django.shortcuts import render,get_object_or_404
from store.models import Category,Product
# Create your views here.
def index(request, category_slug=None):
    products = None
    category_page = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.all().filter(category = category_page, available = True)
    else:
        products = Product.objects.all().filter(available = True)

    return render(request,'index.html',{'products':products, 'categoty':category_page})

def product(request):
    return render(request, 'product.html')