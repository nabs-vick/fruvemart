from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import SignUpForm, ProductForm
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Feedback, Product, Category, Customer,Order,Cart_components
from fruit_app.credentials import LipanaMpesaPpassword, MpesaAccessToken
import requests
import json
from django.http import HttpResponse
# Create your views here.


def index(request):   
    products = Product.objects.all()
    return render(request,'index.html',{'products':products})


@user_passes_test(lambda user: user.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('fruit_app:index')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser)
# Remove a product
def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('fruit_app:index')

@user_passes_test(lambda user: user.is_superuser)
# Update a product 
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('fruit_app:index')
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form})


def shop(request):
    products=Product.objects.all()
    return render(request,'shop.html',{'products':products})
# above code is for the products


def testimonials(request):
    return render(request,'testimonial.html')


@login_required(login_url='fruit_app:login')
def contact(request):
    """to collect feedbacks from the users"""
    if request.method == 'POST':
        connect= Feedback(
            name = request.POST['name'],
            email = request.POST['email'],
            message = request.POST['message']
        )
        connect.save()
        messages.success(request,'thank you for the feedback')
        return redirect('fruit_app:index')
    else:
        return render(request,'contact.html')
    

# above code is for the feedback of the user 


@login_required(login_url='fruit_app:login')
def checkout(request):
    if request.method == 'POST':
        # Create a Cart_components object with data from the form in the html
        components = Cart_components(
            name=request.POST.get('name'),
            product_name=request.POST.get('product_name'),
            product_img=request.POST.get('product_img'),  # Ensure this matches your input field
            address=request.POST.get('address'),
            town=request.POST.get('town'),
            phone_num=request.POST.get('phone_num'),
            price=request.POST.get('price'),
            message=request.POST.get('message'),
            user=request.user,  # Associate with the logged-in user
        )
        # Validate the data manually 
        try:
            components.full_clean()  # Validates the model fields
            components.save()        # Save the instance
            messages.success(request, 'Order submitted successfully!')
            return redirect('fruit_app:cart')  # Redirect after successful submission
        except Exception as err:
            # Handle validation errors or other exceptions
            messages.error(request, f"An error occurred: {err}")
            return render(request, 'checkout.html', {'error': str(err)})

    # If the request method is not POST, render the checkout form
    return render(request, 'checkout.html')





@login_required(login_url='fruit_app:login')
def cart(request):
    """ fetch all orders """
    if request.user.is_staff:
        components=Cart_components.objects.all()
    else:
        # Create a variable to store these pick-up details
        components = Cart_components.objects.filter(user=request.user)
    context = {
        'components':components
        }
    return render(request, 'cart.html', context)

def delete_order(request,id):
    """ Deleting order in cart """
    components = Cart_components.objects.get(id=id) # fetch the particular appointment by its ID
    components.delete() # actual action of deleting
    return redirect("fruit_app:cart") # just remain on the same page

def update_order(request, id):
    """ Update the orders in cart """
    components = get_object_or_404(Cart_components, id=id)
    # Put the condition for the form to update
    if request.method == 'POST':
        components.name = request.POST.get('name')
        components.product_name = request.POST.get('product_name')
        components.phone_num = request.POST.get('phone_num')
        components.address = request.POST.get('address')
        components.product_img = request.POST.get('product_img')
        components.town = request.POST.get('town')
        components.message = request.POST.get('message')
        # Once you click on the update button
        components.save()

        return redirect("fruit_app:cart")
    
    context = {'components': components}
    return render(request, "update_order.html", context)


def page404(request):
    return render (request,'404.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('logged in successfully'))
            return redirect('fruit_app:index')
        else:
            messages.success(request, ('something went wrong'))
            return redirect('fruit_app:login')
    else:
        return render(request,'login.html')

def logout_view(request):
    logout(request,)
    messages.success(request, ('you have logged out successfully'))
    return redirect('fruit_app:index')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,('Registered successfully'))
            return redirect('fruit_app:index')
        else:
            messages.error(request,('error'))
            return render(request,'register.html',{'form':form})
    return render(request,'register.html', {'form': form})



@login_required(login_url='fruit_app:login')
def description(request,id):
    product = Product.objects.get(id=id)
    return render(request,'shop-detail.html',{'product':product})


def pay(request):
    """ Renders the form to pay """
    return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'BSiGF8UpuHADazYv89oYXuS7o1Icu8Dw03Je5nDfQDxjyLqb'
    consumer_secret = 'KAg5xx58KB3ReNJ4UPuoXaAlqHTOVFcoGChjx2dO4bnmiLvHbGlHAA4385qAo21b'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        # return HttpResponse("Success")
        return redirect('fruit_app:404')


