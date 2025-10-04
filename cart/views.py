from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


from cart import models as cart_model
from django.contrib import messages

from django.db import models
from decimal import Decimal

def index(request):
    products = cart_model.Product.objects.filter(status="Published")
    # category = 

    context = {"products": products}
    return render(request, 'cart/index.html', context)


def add_to_cart(request):
    # get the parameters
    id = request.GET.get("id")
    qty = request.GET.get("qty")
    color = request.GET.get("color")
    size = request.GET.get("size")
    cart_id = request.GET.get("cart_id")
    
    #assign the cart id to a session - remember by default, it doesn't exist
    request.session['cart_id'] = cart_id
    
    # validate required fields
    if not id or not qty or not cart_id:
        return JsonResponse({"error": "No color or size selected"}, status=400) # bad request error
    
    # fetch product
    try:
        product = cart_model.Product.objects.get(status="Published", id=id)

    except cart_model.Product.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404) # Page not found
    
    # check if item is already in the cart
    existing_cart_item = cart_model.Cart.objects.filter(cart_id=cart_id, product=product).first()

    # check if the user quantity exceeds the given quantity
    if int(qty) > product.stock:
        return JsonResponse({"error": "Quantity exceeds stock amount"}, status=404)

    # if the item is not in the cart, create one
    if not existing_cart_item:
        cart = cart_model.Cart() # create a new cart item
        cart.product = product
        cart.qty = qty
        cart.price = product.price
        cart.color = color
        cart.size = size
        cart.sub_total = Decimal(product.price) * Decimal(qty)
        cart.shipping = Decimal(product.shipping) * Decimal(qty)
        cart.total = cart.sub_total + cart.shipping
        cart.user = request.user if request.user.is_authenticated else None
        cart.cart_id = cart_id
        cart.save()

        message = "Item added to cart"
    else:
        # if the item exists, update it
        existing_cart_item.qty = qty
        existing_cart_item.price = product.price
        existing_cart_item.color = color
        existing_cart_item.size = size
        existing_cart_item.sub_total = Decimal(product.price) * Decimal(qty)
        existing_cart_item.shipping = Decimal(product.shipping) * Decimal(qty)
        existing_cart_item.total = existing_cart_item.sub_total + existing_cart_item.shipping
        existing_cart_item.user = request.user if request.user.is_authenticated else None
        existing_cart_item.cart_id = cart_id
        existing_cart_item.save()

        message = "Cart Updated"

    total_cart_items = cart_model.Cart.objects.filter(cart_id=cart_id).count() # get the total cart items
    cart_sub_total = cart_model.Cart.objects.filter(cart_id=cart_id).aggregate(sub_total = models.Sum('sub_total'))['sub_total'] # get the cart sub total

    # Return the response to the user    
    return JsonResponse({
        "message": message,
        "total_cart_items": total_cart_items,
        "cart_sub_total": "{:,.2f}".format(cart_sub_total), # {:,.2f} -> creates comas(,) and decimal points(.) to amounts
        "item_sub_total": "{:,.2f}".format(existing_cart_item.sub_total) if existing_cart_item else "{:,.2f}".format(cart.sub_total) # get the item sub total
    })
        

# Cart functions
def cart(request):
    if 'cart_id' in request.session: # check if cart id exists in session
        cart_id = request.session['cart_id'] # create a new cart id
    
    else:
        cart_id = None
        
    items = cart_model.Cart.objects.filter(cart_id=cart_id) # get all the cart items from the session
    cart_sub_total = cart_model.Cart.objects.filter(cart_id=cart_id).aggregate(sub_total = models.Sum('sub_total'))['sub_total'] # get the cart sub total

    if not items:
       messages.warning(request, "Your cart is empty")
       return redirect('cart:index')
    
    context = {
        "items": items,
        "cart_sub_total": cart_sub_total,
    }
    return render(request, 'cart/cart.html', context)

# delete cart item
def delete_cart_item(request):
    # get the parameters
    id = request.GET.get("id")
    item_id = request.GET.get("item_id")
    cart_id = request.GET.get("cart_id")
    
    # validate required fields
    if not id and not item_id and not cart_id:
        return JsonResponse({"error": "No item id or cart id found"}, status=400) # bad request error
    
    try:
        product = cart_model.Product.objects.get(status="Published", id=id)
        
    except cart_model.Product.DoesNotExist:
        return JsonResponse({"error": "Page not found"}, status=404) # Page not found
    
    # check if the item exists
    item = cart_model.Cart.objects.get(product=product, id=item_id) 
    item.delete()

    # Count the remaining items in the cart
    total_cart_items = cart_model.Cart.objects.filter(cart_id=cart_id).count() # get the total cart items
    cart_sub_total = cart_model.Cart.objects.filter(cart_id=cart_id).aggregate(sub_total = models.Sum('sub_total'))['sub_total'] # get the cart sub total

    # Return the response to the user    
    return JsonResponse({
        "message": "Item Deleted",
        "total_cart_items": total_cart_items,
        "cart_sub_total": "{:,.2f}".format(cart_sub_total) if cart_sub_total else 0.00 , # {:,.2f} -> creates comas(,) and decimal points(.) to amounts
    })
    
# Create product
def create_product(request):

    categories = cart_model.Category.objects.all() # get all the categories
    
    if request.method == "POST":
        image = request.FILES.get("image")
        name = request.POST.get("name")
        category_id = request.POST.get("category_id")
        description = request.POST.get("description")
        price = request.POST.get("price")
        regular_price = request.POST.get("regular_price")
        shipping = request.POST.get("shipping")
        stock = request.POST.get("stock")
        
        # Now Create the product
        product = cart_model.Product.objects.create(
            name = name,
            image = image,
            category_id = category_id,
            description = description,
            price = price,
            regular_price = regular_price,
            shipping = shipping,
            stock = stock,
        )
        # product.save()
        
        messages.success(request, "Product created successfully")
        return redirect('cart:update_product', product.id)
    
    return render(request, 'cart/create_product.html', {"categories": categories})

# Update product
def update_product(request, id):
    # get the product and its Id
    product = get_object_or_404(cart_model.Product, id=id)
    categories = cart_model.Category.objects.all()

    if request.method == "POST":
        image = request.FILES.get("image")
        name = request.POST.get("name")
        category_id = request.POST.get("category_id")
        description = request.POST.get("description")
        price = request.POST.get("price")
        regular_price = request.POST.get("regular_price")
        shipping = request.POST.get("shipping")
        stock = request.POST.get("stock")


        # Update the Product Details
        product.name = name
        product.category_id = category_id
        product.description = description
        product.price = price
        product.regular_price = regular_price
        product.shipping = shipping
        product.stock = stock
        if image: # image will be updated only if new one is uploaded
            product.image = image
        product.save()


        # Handle product variant and items - create a function that will iterate the products and variants 
        variant_ids = request.POST.getlist('variant_id[]') # 
        # the purpose of using getlist is because the its going to be in a list 
        variant_titles = request.POST.getlist('variant_title[]')

        # check if variant_ids and variant_titles exists
        if variant_ids and variant_titles:
            # Loop through the variants
            # Looping with enumerate will maintain the structure and the ids will be assigned to i as whenever an item is selected it will grab the id same time cos the ids has been assigned to the variable which is the i
            for i, variant_id in enumerate(variant_ids): # variant_ids represent the values
                # i represents index which will start from 0 while variant_is is the actual value
                variant_name = variant_titles[i] # i has been assigned ti variant_name
                
                # If variant exists, update it
                if variant_id:
                    variant = cart_model.Variant.objects.filter(id=variant_id).first() # grab the first one
                    
                    # if the variant for the id/item exists
                    if variant:
                        variant.name = variant_name # update it
                        variant.save()
                
                else:
                    # if it does not exists but the user is trying to fill a new one, create new variant 
                    variant = cart_model.Variant.objects.create(product=product, name=variant_name)

                # Now handle items for this variant - we are using the array method [] cos the user might add multiple variants
                item_ids = request.POST.getlist(f'item_id_{i}[]') # get the list items passing the (i) which is the selected id/variant using the f string method - [] is a method along with getlist
                item_titles = request.POST.getlist(f'item_title_{i}[]') # get the list item_titles passing the (i) which is the selected id/variant using the f string method - [] is a method along with getList
                item_descriptions = request.POST.getlist(f'item_description_{i}[]') # get the list item_descriptions passing the (i) which is the selected id/variant using the f string method - [] is a method along with getList

                if item_ids and item_titles and item_descriptions: # check if they exists 

                    #  Loop through them and check the fields for existing items using the variable j as the parameter 
                    for j in range(len(item_titles)):
                        item_id = item_ids[j]
                        item_title = item_titles[j]
                        item_description = item_descriptions[j]
                        
                        # if any exists, update it
                        if item_id:
                            variant_item = cart_model.VariantItem.objects.filter(id=item_id).first() # grab the first one

                            if variant_item: # if variant also exists, update it
                                variant_item.title = item_title
                                variant_item.content = item_description
                                variant_item.save()
                        
                        else: # if not, Create new item
                            cart_model.VariantItem.objects.create(
                                variant=variant,
                                title=item_title,
                                content=item_description
                            )
                            
        # Product Gallery Images
        # Get all dynamically added image input
        for file_key, image_file in request.FILES.items(): # file_key -> handles the image field e.g(image1, image2). - image_file -> handles the image that was uploaded
        #  this (request.FILES.items()) line of code handles multiple images
            if file_key.startswith('image_'): # identifying the dynamically added image inputs e.g data_/_image_
                cart_model.Gallery.objects.create(product=product, image=image_file)
                # if all conditions are m,et, create the product with its images
                
        # redirect back to the updated pafe after saving
        messages.success(request, "Product Updated Successfully")
        return redirect("cart:update_product", product.id)

    context = {
        "product": product,
        "categories": categories,
        "variants": cart_model.Variant.objects.filter(product=product),
        "gallery_images": cart_model.Gallery.objects.filter(product=product),
    }
    
    return render(request, "cart/update_product.html", context)
                    
                        
# Delete Variant
def delete_variants(request, product_id, variant_id):
    product = cart_model.Product.objects.get(id=product_id) # get the product id
    variants = cart_model.Variant.objects.get(product=product, id=variant_id) 
    variants.delete()
    return JsonResponse({"message": "Variants deleted"})

# Delete Variants Items
def delete_variants_items(request, variant_id, item_id):
    variant = cart_model.Variant.objects.get(id=variant_id) # get the variant that belong to that id
    item = cart_model.VariantItem.objects.get(variant=variant, id=item_id) # get the varient item that belong to that id
    item.delete()
    return JsonResponse({"message": "Variant item deleted"})

# Delete Product Image
def delete_product_image(request, product_id, image_id):
    product = cart_model.Product.objects.get(id=product_id) # get the product that belong to that id
    item = cart_model.Gallery.objects.get(product=product, id=image_id) # get the product and the gallery that belong to that id 
    item.delete()
    return JsonResponse({"message": "Product image deleted"})

# Delete Product 
def delete_product(request, product_id):
    product = cart_model.Product.objects.get(id=product_id) # get the product that belong to that id
    product.delete()

    messages.success(request, "Product Deleted ")
    return redirect("/")




                    
                    


        











   
        