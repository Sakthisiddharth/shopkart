from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q



def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'auth/login.html')






def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'auth/register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        return redirect('home')

    return render(request, 'auth/register.html')





def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})




def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def increase_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')



@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, completed=False).first()
    return render(request, 'cart.html', {'order': order})


@login_required
def checkout(request):
    order = Order.objects.filter(
        user=request.user,
        completed=False
    ).first()

    if not order:
        return redirect('cart')

    if request.method == 'POST':
        order.completed = True
        order.status = 'Pending'
        order.save()
        return redirect('order_status')

    return render(request, 'checkout.html', {'order': order})



@login_required
def product_buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        address = request.POST.get('address')

        order = Order.objects.create(
            user=request.user,
            completed=True,
            status='Pending'
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

        return redirect('order_success')

    return render(request, 'product_buy.html', {
        'product': product
    })


def order_success(request):
    return render(request, 'order_success.html')



def search_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'search_results.html', {
        'products': products,
        'query': query
    })


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)



    total = 0   
    for item in cart_items:
        total += item.total_price()

    context = {
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'cart.html', context)

@login_required
def dummy_buy(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    product = cart_item.product

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        address = request.POST.get('address')

        # Create order
        order = Order.objects.create(
            user=request.user,
            completed=True,
            status='Pending'
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

        # Remove item from cart
        cart_item.delete()

        return redirect('order_success')

    return render(request, 'cart_buy.html', {'product': product})



@login_required
def order_status(request):
    orders = Order.objects.filter(user=request.user,completed=True).order_by('-created_at')

    return render(request, 'order_status.html', {'orders': orders})


def about(request):
    return render(request, 'about.html')
