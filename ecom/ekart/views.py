from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import products, cart, Order


# Create your views here.

def home(request):
    return render(request,'index.html',{})

def auth(request):
    return render(request,'auth.html',{})

def signup(request):
    if request.method=='POST':
       user = request.POST['email']
       password = request.POST['password']
       full_name = request.POST['full_name']
       first_name = full_name.split(' ')[0]
       last_name = full_name.split(' ')[1]

       users = User.objects.create_user(username=user,password=password, email=user, first_name=first_name, last_name=last_name)
       print("User created Successfully !!!", users)
       return redirect('/')
    
def signin(request):
    if request.method=='POST':
        Username = request.POST['email']
        password = request.POST['password']

        #login
        User = authenticate(request,username=Username, password=password)

        if User is not None:
            login(request, User)
            print("user login successful", User)
            return redirect('/')
        else:
            return redirect('/auth')
        
def shop(request):
    product = products.objects.all()
    return render(request, 'shop.html', {"product":product})

def add_cart(request, product_id):
    if request.user.is_authenticated:
        try:
            existing_cart = cart.objects.get(user=request.user)
            if existing_cart:
                # add product to that cart
                existing_cart.product.add(product_id)
                print(f"Product {product_id} is added to the Cart!!")
            else:
                # user does not have any cart yet
                # Create Cart
                new_cart = cart.objects.create(user= request.user)
                # Add product to the cart
                new_cart.product.add(product_id)
                print(f"Product {product_id} is added to the Cart!!")


        except cart.DoesNotExist:
            # user does not have any cart yet
            # Create Cart
            new_cart = cart.objects.create(user= request.user)
            # Add product to the cart
            new_cart.product.add(product_id)
            print(f"Product {product_id} is added to the Cart!!")

    else:
        print("User is not logged in")

    return redirect('/shop')

def cart_p(request):
    if request.user.is_authenticated:
        Cart = cart.objects.get(user = request.user)
        Cart_items = Cart.product.all()
        grand_sum = 0 
        for item in Cart_items:
            grand_sum+=item.price
        return render(request, 'cart.html', {"cart_items":Cart_items, "grand_sum":grand_sum})
    else:
        print('User not logged in')
        return redirect('/auth')
        
def delete_cart_item(request, product_id):
    Cart = cart.objects.get(user= request.user)
    Cart.product.remove(product_id)
    print("Item deleted from Cart!")
    return redirect('/add_cart')

from uuid import uuid4
def checkout(request):
    Cart = cart.objects.get(user = request.user)
    cart_items = Cart.product.all()
    grand_sum = 0 
    for item in cart_items:
        grand_sum+=item.price
    
    # if method is post i.e. Checkout
    if request.method =="POST":
        # create order
        order_id = str(uuid4())
        address = request.POST['address']
        mobile_no = request.POST['mobile_no']

        for item in cart_items:
            Order.objects.create(order_id=order_id,user= request.user, product = item, address =address, mobile_no=mobile_no)
            # remove ordered product from cart
            Cart.product.remove(item)
            
        print("Order Placed!!")
        return redirect('/orders')


    return render(request, 'checkout.html', {'cart_items':cart_items, 'grand_sum':grand_sum})


def Orders_p(request):
    orders = Order.objects.filter(user= request.user).order_by('order_id')

    order_list=[]

    temp_order_id = ''
    total_order_price=0
    for order in orders:
        if temp_order_id != order.order_id:
            temp_order_id = order.order_id
            order_list.append({"order_id":order.order_id, 'order_price':total_order_price, 'status':order.status})
        else:
            total_order_price+= order.product.price
            order_list[-1] = {"order_id":order.order_id, 'order_price':total_order_price, 'status':order.status}

        return render(request, 'orders.html', {"order_list":order_list, "orders":orders})
