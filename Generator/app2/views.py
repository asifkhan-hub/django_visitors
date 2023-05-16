from django.shortcuts import render, redirect, HttpResponse
from .models import Customer, Product, Cart, OrderPlaced,Visitor
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def ProductView(request):

     return render(request, 'app/passhome.html')


def qrcode(request):
    return render(request, 'app/qrcode.html')

@login_required
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


def mobile(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

    from django.contrib import messages

    def post(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        # Check the number of existing passwords for the current user
        existing_passwords_count = Customer.objects.filter(user=request.user).count()

        if existing_passwords_count >= 3:
            # messages.error(request, 'You have reached the maximum limit of saved passwords.')
            return render(request, 'app/money.html')

            form = CustomerProfileForm()
        else:
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                usr = request.user
                Password_Name = form.cleaned_data['Password_Name']
                Password = form.cleaned_data['Password']
                reg = Customer(user=usr, Password_Name=Password_Name, Password=Password)
                reg.save()
                messages.success(request, 'Congratulations!! Password Saved Successfully.')
                form = CustomerProfileForm()

        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})


def generate(request):
    return render(request,'app/index.html')


# def visitor_count(request):
#     total_visitors = Visitor.objects.count()
#     return render(request, 'app/visitor_count.html', {'total_visitors': total_visitors})

def visitor_count(request):
    visitors = Visitor.objects.all()
    return render(request, 'app/visitor_count.html', {'visitors': visitors})