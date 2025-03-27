from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import products, cart, Order, contact, Wishlist
from django.db.models import Q
from uuid import uuid4

# Home Page
def home(request):
    return render(request, 'index.html', {})

# Authentication Page
def auth(request):
    return render(request, 'auth.html', {})

# About Page
def about(request):
    return render(request, 'about us.html', {})

# Blog Page
def blog(request):
    return render(request, 'blog.html', {})

# Contact Page
def contacts(request):
    if request.method == 'POST':
        fname = request.POST['first']
        lname = request.POST['last']
        email = request.POST['email']
        text = request.POST['text']
        contact.objects.create(first_name=fname, last_name=lname, email=email, text=text)
        print(f"Contact added successfully: {fname} {lname}")
        return redirect('/')
    return render(request, 'contact.html', {})

# Services Page
def service(request):
    return render(request, 'service.html', {})

# Signup Function
def signup(request):
    if request.method == 'POST':
        user = request.POST['email']
        password = request.POST['password']
        full_name = request.POST['full_name']
        first_name, last_name = full_name.split(' ', 1)

        users = User.objects.create_user(username=user, password=password, email=user, first_name=first_name, last_name=last_name)
        print("User created successfully!", users)
        return redirect('/')
    return render(request, 'auth.html')

# Signin Function (Login)
def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("User login successful", user)
            next_url = request.GET.get("next", "/")  # Redirect to intended page or home
            return redirect(next_url)
        else:
            return render(request, 'auth.html', {"error": "Invalid username or password."})
    return render(request, 'auth.html')

# Shop Page
def shop(request):
    product_list = products.objects.all()
    return render(request, 'shop.html', {"product": product_list})

# Add to Cart
@login_required(login_url='/login')
def add_cart(request, product_id):
    user_cart, created = cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(products, id=product_id)

    if not user_cart.product.filter(id=product_id).exists():
        user_cart.product.add(product)
        print(f"Product {product_id} added to Cart!")
    else:
        print(f"Product {product_id} is already in the Cart.")

    return redirect('/shop')

# View Cart
@login_required(login_url='/login')
def cart_p(request):
    try:
        user_cart = cart.objects.get(user=request.user)
        cart_items = user_cart.product.all()
        grand_total = sum(item.price for item in cart_items)
        return render(request, 'cart.html', {"cart_items": cart_items, "grand_sum": grand_total})
    except cart.DoesNotExist:
        return render(request, 'cart.html', {"cart_items": [], "grand_sum": 0})

# Remove Cart Item
@login_required(login_url='/login')
def delete_cart_item(request, product_id):
    user_cart = cart.objects.get(user=request.user)
    product = get_object_or_404(products, id=product_id)
    user_cart.product.remove(product)
    print("Item removed from Cart!")
    return redirect('/cart_p')

# Search Product
def search_product(request):
    if request.method == 'POST':
        search_query = request.POST['search-bar']
        filtered_products = products.objects.filter(Q(name__icontains=search_query) | Q(desc__icontains=search_query) | Q(specification__icontains=search_query))
        return render(request, 'product.html', {'products': filtered_products})
    return redirect('/shop')

# Product Detail View
def product(request, pro_id):
    product_details = get_object_or_404(products, id=pro_id)
    return render(request, 'shop-fur.html', {'prod': product_details})

# Wishlist View
@login_required(login_url='/login')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

# Add to Wishlist
@login_required(login_url='/login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(products, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('/view_wishlist')

# Remove from Wishlist
@login_required(login_url='/login')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(products, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('/view_wishlist')

# Checkout
@login_required(login_url='/login')
def checkout(request):
    try:
        user_cart = cart.objects.get(user=request.user)
        cart_items = user_cart.product.all()
        grand_total = sum(item.price for item in cart_items)

        if request.method == "POST":
            order_id = str(uuid4())
            address = request.POST['address']
            mobile_no = request.POST['mobile_no']

            for item in cart_items:
                Order.objects.create(order_id=order_id, user=request.user, product=item, address=address, mobile_no=mobile_no)
                user_cart.product.remove(item)

            print("Order Placed Successfully!")
            return redirect('/orders')

        return render(request, 'checkout.html', {'cart_items': cart_items, 'grand_sum': grand_total})
    except cart.DoesNotExist:
        return render(request, 'checkout.html', {'cart_items': [], 'grand_sum': 0})

# Orders Page
@login_required(login_url='/login')
def Orders_p(request):
    orders = Order.objects.filter(user=request.user).order_by('order_id')
    order_list = []
    temp_order_id = None
    total_order_price = 0

    for order in orders:
        if temp_order_id != order.order_id:
            if temp_order_id is not None:
                order_list.append({"order_id": temp_order_id, "order_price": total_order_price, "status": order.status})

            temp_order_id = order.order_id
            total_order_price = order.product.price
        else:
            total_order_price += order.product.price

    if temp_order_id is not None:
        order_list.append({"order_id": temp_order_id, "order_price": total_order_price, "status": orders.last().status})

    return render(request, 'orders.html', {"order_list": order_list, "orders": orders})
