from django.shortcuts import render, redirect, resolve_url
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from product.models import Product, ProductTransaction
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.


class Products(LoginRequiredMixin, View):
    def get(self, request):
        all_products = Product.objects.all().order_by("-created_at")
        context = {
            "all_prod": all_products
        }
        return render(request, "products.html", context)
    
class AddProduct(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "add_product.html")
    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        print(request.FILES)
        print(name, description, quantity, price, image)
        if not name or not description or not quantity or not price or not image:
            messages.error(request, "All fields are required")
            return redirect(resolve_url('add-product'))
        try:
            price = int(price)
            quantity = int(quantity)
        except:
            messages.error(request, "Price and quantity must be integer")
            return redirect(resolve_url('add-product'))

        
        if price < 1:
            messages.error(request, "Price too low")
            return redirect(resolve_url('add-product'))
        if quantity < 1:
            messages.error(request, "Quantity too low")
            return redirect(resolve_url('add-product'))
        Product.objects.create(
            name = name, 
            description = description,
            price = price, 
            quantity = quantity,
            image = image,
            user = request.user
        )
        messages.success(request, "Product listed successfully!")
        return redirect(resolve_url("products"))

class EditProduct(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return redirect(resolve_url('products'))
        if product.user != request.user:
            return redirect(resolve_url('products'))
        context = {"product": product}
        return render(request, "edit_product.html", context)
    def post(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return redirect(resolve_url('products'))
        if product.user != request.user:
            return redirect(resolve_url('products'))
        
        name = request.POST.get("name")
        description = request.POST.get("description")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        image = request.FILES.get("image")

        product.name = name or product.name
        product.description = description or product.name
        product.quantity = quantity or product.quantity
        product.price = price or product.price
        product.image = image or product.image
        product.save()
        messages.success(request, "Product successfully updated")
        return redirect(resolve_url('products'))
        
@login_required
def delete_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return redirect(resolve_url('products'))
    if product.user != request.user:
        return redirect(resolve_url('products'))
    product.delete()
    messages.success(request, "Product successfully removed")
    return redirect(resolve_url('products'))


def list_products(request):
    all_products = Product.objects.all()
    data = [{"name": x.name, "id": x.id, "quantity": x.quantity, "image": x.image.url} for x in all_products]
    return JsonResponse(data, safe=False)

@login_required
def buy_product(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return redirect(resolve_url('products'))
    if product.user == request.user:
        messages.error(request, "Why are you buying your own product????????")
        return redirect(resolve_url('products'))
    if request.method == "POST":
        quantity = request.POST.get("qty")
        try:
            quantity = int(quantity)
        except:
            messages.error(request, "quantity must be integer")
            return redirect(resolve_url('products'))
        if product.quantity < quantity:
            messages.error(request, "quantity more than what we have in stock")
            return redirect(resolve_url('products'))
        # product.quantity -= quantity
        product.quantity = product.quantity - quantity
        product.sold += quantity

        ProductTransaction.objects.create(
            quantity = quantity,
            quantity_after = product.quantity,
            product = product,
            user = request.user,
            price = product.price
        )
        product.save()
        messages.success(request, "Product bought successfully!")
        return redirect(resolve_url('products'))
    return render(request, "buy-product.html")

@login_required
def product_transactions(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return redirect(resolve_url('products'))
    if product.user != request.user:
        return redirect(resolve_url('products'))
    transactions = ProductTransaction.objects.filter(product=product).order_by("-created_at")
    context = {"transactions": transactions}
    return render(request, )


def error_404(request, exception):
    return render(request, "error_404.html")

def error_500(request):
    return render(request, "error_500.html")