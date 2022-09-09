from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CartItem,Cart
from products.models import Product
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()
paypal_url = os.getenv('paypal_url')
paypal_client_id = os.getenv('paypal_client_id')
paypal_client_secret = os.getenv('paypal_client_secret')
@login_required(login_url='login_user')
# Create your views here.
def get_cart(request):
    if request.user.is_authenticated:
        products = request.user.cart.products.all()
        total = 0
        for cartItem in products:
            total += cartItem.product.price * cartItem.amount
        return render(request, "user/cart.html", {
            "products": products,
            "total": total,
            "client_id": paypal_client_id,
            "client_token": generate_client_token()
        })
    return redirect("/")

@login_required(login_url='login_user')
def add_to_cart(request, idProduct):
    if request.user.is_authenticated:
        cartItem = CartItem()
        cartItem.product = Product.objects.get(pk=idProduct)
        cartItem.amount = 1
        cartItem.cart = request.user.cart

        cartItem.save()

    return redirect("/")

@csrf_exempt
def change_amount(request):
    if request.method == "POST":
        data = json.loads(request.body)

        amount = data['amount']
        id_item = data['idItem']

        cart_item = CartItem.objects.get(id=id_item)

        cart_item.amount = amount
        cart_item.save()
        
        cart_items = cart_item.cart.products.all()

        total = 0
        for cartItem in cart_items:
            total += cartItem.product.price * cartItem.amount

        return JsonResponse({
            "total": total
        })


def delete_from_cart(request, id_cart_item):
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(pk=id_cart_item)
        if cart_item.cart.user == request.user:
            cart_item.delete()

            return redirect("/cart")

    return redirect("/")

    

@csrf_exempt
def create_paypal_order(request):
    products = request.user.cart.products.all()
    total = 0
    for cartItem in products:
        total += cartItem.product.price * cartItem.amount

    access_token = get_access_token()
    create_order_url = paypal_url+"/v2/checkout/orders"
    response = requests.post(create_order_url, headers={
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }, data=json.dumps({
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": total
                }
            }
        ]
    }))

    data = response.json()

    return JsonResponse({
        "order": data
    })


@csrf_exempt
def capture_paypal_order(request, order_id):
    access_token = get_access_token()
    capture_order_url = paypal_url+"/v2/checkout/orders/"+order_id+"/capture"
    response = requests.post(capture_order_url, headers={
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    })

    data = response.json()
    print(data)
    cart_items = request.user.cart.delete()
    new_cart = Cart()
    new_cart.user = request.user
    new_cart.save()

    return JsonResponse(data)




def get_access_token():
    access_token_url = paypal_url + "/v1/oauth2/token"
    response = requests.post(access_token_url,data={
        "grant_type": "client_credentials",
    }, auth=HTTPBasicAuth(paypal_client_id, paypal_client_secret))

    data = response.json()

    return data['access_token']




def generate_client_token():
    access_token = get_access_token()

    client_token_url = paypal_url + "/v1/identity/generate-token"
    response = requests.post(client_token_url, headers={
        "Authorization": "Bearer "+access_token,
        "Accept-Language": "en_US",
        "Content-Type": "application/json",
    })

    data = response.json()

    return data['client_token']