from django.shortcuts import render, redirect
from products.models import Category
from products.models import Product
# Create your views here..
def home(request):
    category = request.GET.get('categoria','')
    if category == '':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            categories__name = category
        )

    categories = Category.objects.all()
    return render(request, "home.html",{
        "products": products,
        'categories':categories
    })

def search(request):
    categories = Category.objects.all()
    if request.method == "POST":
        q=request.POST ['search']
        
        products = Product.objects.filter(name__icontains=q)
        print(products)
        return render(request, "home.html",{
        "products": products,
        'categories':categories
        })
