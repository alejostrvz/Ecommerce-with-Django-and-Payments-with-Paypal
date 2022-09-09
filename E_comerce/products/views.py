from django.shortcuts import render, redirect
from .models import Product, Review
from .models import Category

def detail_product(request, id):
    product = Product.objects.get(id=id)
    reviews = Review.objects.filter(product=product.id)
    
    return render(request, 'products/detail_product.html', {'product':product, 'reviews':reviews})




def create_review(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        review = Review(
            product = product,
            content = request.POST['rev_content'],
            author = request.user
        )

        review.save()

        return redirect("/products/" + str(product.id))

    return redirect('/')

def delete_review(request, id):
    review = Review.objects.get(id=id)
    id_product = review.product.id
    review.delete()

    return redirect('/products/' + str(id_product))