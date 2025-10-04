from cart import models as cart_model

def default(request):
    try:
        cart_id = request.session['cart_id'] # check if cart_id exists in session
        total_cart_items = cart_model.Cart.objects.filter(cart_id=cart_id).count() # get total items in cart
    except: 
        total_cart_items = 0 # if cart_id doesn't exist, set total items to 0

    return {
        'total_cart_items': total_cart_items
    }