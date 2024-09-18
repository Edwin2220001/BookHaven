from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Cart, CartItem
from django.contrib.auth.decorators import login_required


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def view_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        cart = Cart.objects.create(user=user)  # Create a new cart if none exists

    cart_items = CartItem.objects.filter(cart=cart)

    # total_price = sum(item.get_total_price() for item in cart_items)
    # return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('book_list')



def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')