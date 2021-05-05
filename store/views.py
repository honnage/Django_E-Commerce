from django.shortcuts import render,get_object_or_404,redirect
from store.models import Category, Product, Cart, CartItem
from store.forms import SignUpForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
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


def productPage(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e :
        raise e

    return render(request, 'product.html',{'product':product})


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def addCart(request, product_id):
   #ดึงสินค้าที่เราซื้อมาใช้งาน
    product=Product.objects.get(id=product_id)
    #สร้างตะกร้าสินค้า
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
     
    try:
        #ซื้อรายการสินค้าซ้ำ
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            #เปลี่ยนจำนวนรายการสินค้า
            cart_item.quantity += 1
            #บันทึก/อัพเดท
            cart_item.save()

    except  CartItem.DoesNotExist:
        #ซื้อรายการสินค้าครั้งแรก
        #บันทึกลงฐานข้อมูล
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.save()
    return redirect('/')


def cartdetail(request):
    total = 0
    counter = 0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,available=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.product.price*item.quantity)
            counter+=item.quantity
    except Exception as e :
        pass
    
    return render(request,'cartdetail.html',
    dict(cart_items=cart_items,total=total,counter=counter))


def removeCart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cartItem = CartItem.objects.get(product = product, cart = cart)

    cartItem.delete()
    return redirect('cartdetail')


def signUpView(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  
            form.save()
            username = form.cleaned_data.get('username')
            singUpUser = User.objects.get(username = username)
            customer_group = Group.objects.get(name="Customer")
            customer_group.user_set.add(singUpUser)
    else:
        form = SignUpForm()
    return render(request,"signup.html",{'form':form})


def signInView(request):
    if request.method=='POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signUp')
    else:
        form = AuthenticationForm()
    return render(request,"signin.html",{'form':form})