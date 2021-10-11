from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Accounts.models import Customer
from .models import Addresses, Cart, CustomerProfile,State,City
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from Seller.models import Laptop, Mobile, Grocery
from .filters import LaptopFilter, MobileFilter, GroceryFilter
from.forms import CustomerProfileForm,AddressesForm
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy

# Create your views here.
def seller_to_customer_home(request):
    logout(request)
    return redirect('home')
    

def homeview(request):
    template_name='Customer/Customer_Home.html'
    Laptops=Laptop.objects.all()
    Mobiles=Mobile.objects.all()
    Groceries=Grocery.objects.all()

    context={'Laptops':Laptops, 'Mobiles':Mobiles, 'Groceries':Groceries}
    return render(request,template_name,context)


def showlaptop(request):
    records = Laptop.objects.all()
    laptopfilter = LaptopFilter(request.GET, queryset=records)
    rec_per_page = Paginator(laptopfilter.qs, 3)
    page = request.GET.get('page',1)
    # print('PAGE=',page)
    # print(rec_per_page.count)
    # print(rec_per_page.num_pages)
    # print(rec_per_page.page_range)
    try:
        rec = rec_per_page.page(page)
    except PageNotAnInteger:
        rec = rec_per_page.page(1)
    except EmptyPage:
        rec = rec_per_page.page(rec_per_page.num_pages)
    print('filter record', records)
    return render(request, 'Customer/ShowLaptop.html', {'records': rec, 'laptopfilter': laptopfilter})

def showMobile(request):
    records = Mobile.objects.all()
    mobilefilter = MobileFilter(request.GET, queryset=records)
    rec_per_page = Paginator(mobilefilter.qs, 5)
    print('PAGINATOR=', rec_per_page)

    page=request.GET.get('page',1)
    print('PAGE=',page)
    print(rec_per_page.count)
    print(rec_per_page.num_pages)
    print(rec_per_page.page_range)

    try:
        rec = rec_per_page.page(page)
    except PageNotAnInteger:
        rec = rec_per_page.page(1)
    except EmptyPage:
        rec = rec_per_page.page(rec_per_page.num_pages)

    return render(request,'Customer/ShowMobile.html',{'records':rec, 'mobilefilter':mobilefilter})

def showGrocery(request):
    records = Grocery.objects.all()
    groceryfilter = GroceryFilter(request.GET, queryset=records)
    rec_per_page = Paginator(groceryfilter.qs, 3)
    print('PAGINATOR=', rec_per_page)

    page=request.GET.get('page',1)
    print('PAGE=',page)
    print(rec_per_page.count)
    print(rec_per_page.num_pages)
    print(rec_per_page.page_range)

    try:
        rec = rec_per_page.page(page)
    except PageNotAnInteger:
        rec = rec_per_page.page(1)
    except EmptyPage:
        rec = rec_per_page.page(rec_per_page.num_pages)

    return render(request,'Customer/ShowGrocery.html',{'records':rec, 'groceryfilter':groceryfilter})

@login_required(login_url='customerlogin')
def Laptopview(request, pk):
    laptop = Laptop.objects.get(id=pk)
    user = request.user
    print('User :',user.id)
    cst = Customer.objects.get(user=user)
    y = Cart.objects.filter(customer=cst, laptop=laptop).first()
    if y:
        z = y.quantity + 1
        p = y.price / y.quantity
        q = p * z
        y.price = q
        y.quantity = z
        y.save()
        print('Updated!!!')
        return redirect('cartview')
    else:
        Cart.objects.create(customer=cst, laptop=laptop, mobile=None, grocery=None, price=laptop.price, quantity=1)
        print('Created!!!')
    return redirect('cartview')

@login_required(login_url='customerlogin')
def Mobileview(request, pk):
    mobile = Mobile.objects.get(id=pk)
    user = request.user
    cst = Customer.objects.get(user=user)
    y = Cart.objects.filter(customer=cst, mobile=mobile).first()
    if y:
        z = y.quantity + 1
        p = y.price / y.quantity
        q = p * z
        y.price = q
        y.quantity = z
        y.save()
        print('Updated!!!')
        return redirect('cartview')
    else:
        Cart.objects.create(customer=cst, laptop=None, mobile=mobile, grocery=None, price=mobile.price, quantity=1)
        print('Created!!!')
    return redirect('cartview')

@login_required(login_url='customerlogin')
def Groceryview(request, pk):
    grocery = Grocery.objects.get(id=pk)
    user = request.user
    cst = Customer.objects.get(user=user)
    y = Cart.objects.filter(customer=cst, grocery=grocery).first()
    if y:
        z = y.quantity + 1
        p = y.price / y.quantity
        q = p * z
        y.price = q
        y.quantity = z
        y.save()
        print('Updated!!!')
        return redirect('cartview')
    else:
        Cart.objects.create(customer=cst, laptop=None, mobile=None, grocery=grocery, price=grocery.price, quantity=1)
        print('Created!!!')
    return redirect('cartview')


@login_required(login_url='customerlogin')
def Cartview(request):
    user = request.user
    
    # print('User:', user)
    cst = Customer.objects.get(user=user)
    print(cst)
    ord = Cart.objects.filter(customer=cst)
    context={'ord':ord}
    for i in ord:
        if i.laptop_id is not None:
            product_id = i.laptop_id
            product_name_l = Laptop.objects.get(id=product_id)
            context['product_name_l']=product_name_l.name
            print("Laptop", product_name_l.name)
        elif i.mobile_id is not None:
            product_id = i.mobile_id
            product_name_m = Mobile.objects.get(id=product_id)
            print("Mobile", product_name_m.name)
            context['product_name_m']=product_name_m
        elif i.grocery_id is not None:
            product_id = i.grocery_id
            product_name_g = Grocery.objects.get(id=product_id)
            print("Mobile", product_name_g)
            context['product_name_g']=product_name_g
            print(product_id)
        # context = {'ord': ord, 'product_name_m': product_name_m.name, 'product_name_l': product_name_l.name,'product_name_g':product_name_g}
    template_name = 'Customer/showCart.html'
    
    return render(request, template_name, context)


@login_required(login_url='login')
def Deleteitemview(request, pk):
    # item=Order_item.objects.get(id=pk)
    # item.delete()
    # return redirect('cartview')
    y = Cart.objects.get(id=pk)
    if y.quantity > 1:
        z = y.quantity - 1
        p = y.price / y.quantity
        q = p * z
        y.price = q
        y.quantity = z
        y.save()
        print('Updated!!!')
        return redirect('cartview')
    else:
        print('Deleted!!')
        y.delete()
    return redirect('showcart')


def Updateallitemview(request, pk):
    y = Cart.objects.filter(id=pk).first()
    if y:
        z = y.quantity + 1
        p = y.price / y.quantity
        q = p * z
        y.price = q
        y.quantity = z
        y.save()
        print('Updated!!!')
        return redirect('cartview')


@login_required(login_url='customerlogin')
def create_profile(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerProfileForm()
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = customer
            # obj.address=form.cleaned_data['flat']+', '+form.cleaned_data['area']+', '+form.cleaned_data['landmark']
            obj.full_name=form.cleaned_data['first_name']+' '+form.cleaned_data['last_name']
            obj.save()
            print("object get",obj)
            return redirect('showprofile')
    template_name = 'Customer/Customer_Profile.html'
    context = {'form': form}
    return render(request, template_name, context)



def update_profile(request,id):
    customer = Customer.objects.get(user=request.user)
    record = CustomerProfile.objects.get(id=id)
    form = CustomerProfileForm(instance=record)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST,instance=record)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = customer
            # obj.address=form.cleaned_data['flat']+', '+form.cleaned_data['area']+', '+form.cleaned_data['landmark']
            # obj.full_name=form.cleaned_data['first_name']+' '+form.cleaned_data['last_name']
            obj.save()
            print("object get",obj)
            return redirect('showprofile')
    template_name = 'Customer/Customer_Profile.html'
    context = {'form': form}
    return render(request, template_name, context)





@method_decorator(login_required,name='put')
class CustomerAddressUpdateView(UpdateView):
    model=Addresses
    fields=['country','Mobile_no','state','city','pin_code','flat','area','landmark']
    success_url=reverse_lazy('showaddress')
    template_name='Customer/Customer_Address.html'


@login_required(login_url='customerlogin')
def show_profile(request):
    customer = Customer.objects.get(user=request.user)
    record=CustomerProfile.objects.filter(customer=customer)
    print("Profile record",record)
    template_name='Customer/Show_Customer_Profile.html'
    context={'record':record}
    return render(request,template_name, context)




@login_required(login_url='customerlogin')
def create_address(request):
    customer = Customer.objects.get(user=request.user)
    customer=CustomerProfile.objects.get(customer=customer)
    form = AddressesForm()
    if request.method == 'POST':
        form = AddressesForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = customer
            # obj.address=form.cleaned_data['flat']+', '+form.cleaned_data['area']+', '+form.cleaned_data['landmark']
            obj.save()
            return redirect('showaddress')
    template_name = 'Customer/Customer_Address.html'
    context = {'form': form}
    return render(request, template_name, context)



@login_required(login_url='customerlogin')
def delete_address(request,id):
    record = Addresses.objects.get(id=id)
    record.delete()
    return redirect('showaddress')


@login_required(login_url='customerlogin')
def show_addresses(request):
    customer = Customer.objects.get(user=request.user)
    print(customer.name)
    customer=CustomerProfile.objects.get(customer=customer)
    print(customer.first_name,customer.last_name)
    record=Addresses.objects.filter(customer=customer)
    # print(record.customer)
    template_name='Customer/Show_Customer_Address.html'
    context={'record':record}
    # print(record)
    return render(request,template_name, context)



# AJAX
def load_states(request):
    country_id = request.GET.get('country')
    print(country_id)
    states = State.objects.filter(country_id=country_id).order_by('state_name')
    print([s for s in states])
    return render(request, 'Customer/StateList.html', {'states': states})

def load_cities(request):
    state_id = request.GET.get('state')
    print(state_id)
    cities = City.objects.filter(state_id=state_id).order_by('city_name')
    print([city for city in cities])
    return render(request, 'Customer/CityList.html', {'cities': cities})



@login_required(login_url='customerlogin')
def profile_page(request):
    return render(request,'Customer/Profile_base.html')