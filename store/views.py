from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages, auth

def index(request):
    prods = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        cart, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = cart.orderitem_set.all()
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'products': prods, 'order': cart, 'items': items}
    return render(request, 'index.html', context)


def products(request):
    prods = Product.objects.all()
    cats = Category.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        cart = Order.objects.get(customer=customer, complete=False)
        items = cart.orderitem_set.all()
    else:
        items = []
        cart = {'get_cart_total': 0, 'ge_cart_items': 0}
    context = {'products': prods, 'order': cart, 'items': items, 'categories': cats}
    return render(request, 'products.html', context)


def product(request):
    context = {}
    return render(request, 'product.html', context)


def cart(request):
    customer = request.user.customer
    cart = Order.objects.get(customer=customer, complete=False)
    items = cart.orderitem_set.all()
    context = {'order': cart, 'items': items}
    return render(request, 'cart.html', context)
    

def checkout(request):
    customer = request.user.customer
    cart = Order.objects.get(customer=customer, complete=False)
    items = cart.orderitem_set.all()
    context = {'order': cart, 'items': items}
    return render(request, 'checkout.html', context)


def add_to_cart(request, pk):
    product = Product.objects.get(id=pk)
    customer = request.user.customer
    order = Order.objects.get(customer=customer, complete=False)
    new_item = OrderItem(product = product, order = order, quantity=1)
    new_item.save()
    return redirect("/")

def category(request, pk):
    category = Category.objects.get(cat_name=pk)
    cats = Category.objects.all()
    prods = Product.objects.filter(category=category)
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        cart, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = cart.orderitem_set.all()
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'products': prods, 'order': cart, 'items': items, 'categories': cats}
    return render(request, 'category.html', context)

def search_results(request):
    if request.method == 'POST':
        search_string = request.POST['search']
        cats = Category.objects.all()
        prods = Product.objects.filter(name__contains=search_string)
        if request.user.is_authenticated:
            customer = request.user.customer
            print(customer)
            cart, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = cart.orderitem_set.all()
        else:
            items = []
            cart = {'get_cart_total': 0, 'get_cart_items': 0}
        context = {'products': prods, 'order': cart, 'items': items, 'categories': cats}
        return render(request, 'results.html', context)
    else:
        return render(request, 'results.html')


def login(request):
    if request.method == "POST":
        entered_username = request.POST['username']
        entered_password = request.POST['password']

        user = auth.authenticate(username=entered_username, password=entered_password)
        if user is None:
            messages.info(request, "Invalid Credentials. Please try again")
            return redirect("login")
        else:
            auth.login(request, user)
            return redirect("/")
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        entered_username = request.POST['username'] 
        entered_firstname = request.POST['firstname'] 
        entered_lastname = request.POST['lastname'] 
        entered_phone = request.POST['phone'] 
        entered_email = request.POST['email'] 
        entered_password = request.POST['password'] 
        entered_password2 = request.POST['password2'] 

        if entered_password == entered_password2:
            if User.objects.filter(username=entered_username).exists():
                messages.info(request, "Username already exists")
                return redirect("signup")

            elif User.objects.filter(email=entered_email).exists():
                messages.info(request, "Email is already in use.")
                return redirect("signup")

            else:
                user = User.objects.create_user(username=entered_username, email=entered_email, password=entered_password)
                user.save()
                customer = Customer(user=user, firstname=entered_firstname, lastname=entered_lastname, email=entered_email, phone=entered_phone)
                customer.save()
                return redirect ("login")
        else:
            messages.info(request, "Passwords are not matching")
            return redirect("signup")
    else:
        return render(request, 'signup.html')