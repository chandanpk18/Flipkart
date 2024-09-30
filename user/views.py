from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from .models import Product, Category, Order, HelpRequest
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
# Create your views here.

def is_admin(user):
    return user.is_superuser
def is_user(user):
    return user.groups.filter(name='user').exists()
def is_seller(user):
    return user.groups.filter(name='Seller').exists()

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin/')
    elif is_user(request.user):
        return redirect('product_list')
    else:
        return redirect('my_products')

def signout(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user_group = Group.objects.get_or_create(name='user')
            user_group[0].user_set.add(user)
            if user is not None:
                return redirect(login_view)
    else:
        form = SignupForm()
        return render(request, 'signup.html',{'form': form})


def ssignup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user_group = Group.objects.get_or_create(name='Seller')
            user_group[0].user_set.add(user)
            if user is not None:
                return redirect(login_view)
    else:
        form = SignupForm()
        return render(request, 'Sellsign.html',{'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request,'home.html')

@login_required(login_url='login')
@user_passes_test(is_seller)
def load_categories(request):
    product_type_id = request.GET.get('product_type_id')
    categories = Category.objects.filter(product_type_id=product_type_id).all()
    return JsonResponse(list(categories.values('id', 'name')), safe=False)


def privacy(request):
    return render(request,'privacypolicy.html')

def condition(request):
    return render(request,'termsofuse.html')

def store(request):
    return render(request,'store.html')

@login_required(login_url='login')
@user_passes_test(is_seller)
def seller(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
            return redirect('seller')
    else:
        form = ProductForm()

    return render(request, 'seller.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(is_seller)
def my_products(request):
    user = request.user
    products = Product.objects.filter(added_by=user)
    return render(request, 'my_product.html', {'products': products})

@login_required(login_url='login')
@user_passes_test(is_seller)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk, added_by=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'my_product.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(is_seller)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, added_by=request.user)

    if request.method == 'POST':
        product.delete()
        return redirect('my_products')


def product_list(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=selected_category)
    else:
        products = Product.objects.all()
    return render(request, 'product_list.html', {'categories': categories, 'products': products})

@login_required(login_url='login')
@user_passes_test(is_user)
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Order.objects.create(user=request.user, product=product)

    return redirect('user_orders')

@login_required(login_url='login')
@user_passes_test(is_user)
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'user_orders.html', {'orders': orders})

@login_required(login_url='login')
@user_passes_test(is_user)
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect('user_orders')

def customer_support(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        help_text = request.POST.get('help')
        if username and email:
            help = HelpRequest.objects.create(username=username, email=email, help_text=help_text)
            help.save()
            alert_message = "Your query is submitted successfully."
        return render(request, 'help.html', {'alert_message': alert_message})

    return render(request, 'help.html')