from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from .models import CartItems, Category, Customer, Item, RestCheckout, DueModel, Table, TableCheckout, TableItems
from SAAS.models import *
from django.db.models import Q


def openRestaurantView(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)
    if shopId.user == request.user:
        if shopId.is_active == True:
            category = Category.objects.filter(
                shop=shop_id
            )
            items = Item.objects.filter(
                Q(out_of_stock=False) and Q(shop=shopId)
            )

            cart1 = request.session.get("cart1")
            remove = request.POST.get('remove')
            item_id = request.POST.get("item_id")

            ## Getting all customer

            customers = Customer.objects.filter(
                added_by=request.user
            )

            if item_id is not None:
                if cart1:
                    quantity = cart1.get(item_id)
                    if quantity:
                        if remove:
                            cart1[item_id] = quantity - 1
                        else:
                            cart1[item_id] = quantity + 1
                    else:
                        cart1[item_id] = 1
                    if cart1[item_id] < 1:
                        cart1.pop(item_id)
                else:
                    cart1 = {}
                    cart1[item_id] = 1

                request.session['cart1'] = cart1

                return redirect(f"/restaurant/open-restaurant/{shop_id}/")
            
            # Getting All cart products

            if not cart1:
                request.session.cart1 = {}

            cart_products = None
            
            if cart1:
                ids = list(request.session.get('cart1').keys())
                print(f"{ids=}")
                cart_products = Item.get_items(ids)


            args = {
                "cart_products": cart_products,
                "items": items,
                "category": category,
                "customers": customers,
                "shopId": shopId
            }
            return render(request, "restaurant/openRestaurant.html", args)
        else:
            return HttpResponse("You package has been expired please contact support")
    else:
        return redirect("warning")


def restaurantDueView(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)
    if shopId.user == request.user:

        customers = Customer.objects.all()
        cart1 = request.session.get("cart1", None)
        cart_products = None
        
        if cart1 is not None:
            ids = list(request.session.get('cart1').keys())
            cart_products = Item.get_items(ids)

        if request.method == "POST":
            customer = request.POST.get("selected_due_user")
            order_note = request.POST.get("order_note")
            submission_date = request.POST.get("order_submission_due_date")
            items = cart_products

            year = submission_date.split("/")[2]
            month = submission_date.split("/")[0]
            day = submission_date.split("/")[1]

            submission_date = f"{year}-{month}-{day}"

            # print(submission_date)

            if len(items) <= 0:
                return redirect(f"/restaurant/due-restaurant/{shop_id}/")


            due = DueModel(
                customer=Customer.objects.get(id=customer),
                order_note=order_note,
                submission_date=submission_date,
            )

            due.save()

            due_total = 0

            for item in items:
                quantity = cart1.get(str(item.id))
                due_total += item.item_price * quantity
                cartItems = CartItems(
                    item=item,
                    quantity=quantity
                )
                cartItems.save()
                due.items.add(cartItems)
            
            due.grand_total = due
            due.save()

            # Clearing cookie
            cart1 = {}
            request.session["cart1"] = cart1

            return redirect(f"/restaurant/open-restaurant/{shop_id}/")

        args = {
            "cart_products": cart_products,
            "customers": customers,
            "shopId": shopId,
        }
        return render(request, "restaurant/openRestaurantDue.html", args)
    else:
        return redirect("warning")



def restaurantAvailableTableView(request, shop_id):
    pass
    # shopId = get_object_or_404(Shop, id=shop_id)
    # args = {
    #     "shopId": shopId,
    # }
    # return render(request, "restaurant/availableTable.html", args)

# Add ing new Customer Function
def addingNewCustomer(request, shop_id):
    message = None
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:

        if request.method == "POST":
            data = request.POST
            added_by = request.user
            customer_name = data.get('customer_name')
            customer_contact = data.get('customer_contact')
            customer_email = data.get('customer_email')
            customer_add = data.get('customer_add')
            email_exits = Customer.objects.filter(customer_email=customer_email)
            if not email_exits:
                Customer.objects.create(
                    added_by = User.objects.get(id=request.user.id),
                    customer_name = customer_name,
                    customer_contact = customer_contact,
                    customer_email = customer_email,
                    customer_add = customer_add
                )
                return redirect(f"/restaurant/open-restaurant/{shop_id}/")
            else:
                return HttpResponse("Email Already Registered!")
                
        args = {
            "shop_id": shop_id,
        }
        return render(request, "restaurant/openRestaurant.html", args)

    else:
        return redirect("warning")

# Checkout Function

def get_checkout(request, shop_id):
    cart1 = request.session.get("cart1")
    shopId = Shop.objects.get(pk=shop_id)
    if request.method == "POST":
        ids = list(request.session.get('cart1').keys())

        if len(ids) <= 0:
            return redirect(f"/restaurant/open-restaurant/{shop_id}/")

        cart_products = Item.get_items(ids)
        items = cart_products
        # customer = request.POST.get("customer")
        amount_received = request.POST.get("amount_received")
        change = request.POST.get("change")
        customerId = request.POST.get("customer_id")
        discount = request.POST.get("discount")
        credit_card_number = request.POST.get("credit_card_number")
        bkash_number = request.POST.get("bkash_number")
        nagad_number = request.POST.get("nagad_number")

        # print(type(amount_received))
        # print(type(change))
        # print(credit_card_number)
        # print(bkash_number)
        # print(nagad_number)

        payment_method, payment_number = None, None

        
        if len(credit_card_number) > 0 or len(bkash_number) or len(nagad_number):
            if len(credit_card_number) > 0:
                payment_method = "Credit Card"
                payment_number = credit_card_number
            elif len(bkash_number) > 0:
                payment_method = "bKash"
                payment_number = bkash_number
            elif len(nagad_number) > 0:
                payment_method = "Nagad"
                payment_number = nagad_number
        else:
            payment_method="CASH"

        if customerId or customerId != "":
            checkout = RestCheckout(
                customer=Customer.objects.get(id=customerId),
                amount_received=amount_received,
                change=change,
                discount=discount,
                shop=shopId,
                status="PAID",
                payment_method=payment_method,
                payment_number=payment_number
            )
            checkout.save()
        else:
            checkout = RestCheckout(
                customer=Customer.objects.get(id=5),
                amount_received=amount_received,
                change=change,
                discount=discount,
                shop=shopId,
                status="PAID",
                payment_method=payment_method,
                payment_number=payment_number
            )
            checkout.save()
        grand_total = 0
        for item in items:
            quantity = cart1.get(str(item.id))
            grand_total += item.item_price * quantity
            cartItems = CartItems(
                item=item,
                quantity=quantity
            )
            cartItems.save()
            checkout.items.add(cartItems)
        
        checkout.grand_total = grand_total
        checkout.save()
        # Clearing cookie
        cart1 = {}
        request.session["cart1"] = cart1
        return redirect(f"/restaurant/restaurant-receipt/{shop_id}/{checkout.id}/")
        
    args = {
        "shopId": shopId
    }
    return render(request, "restaurant/openRestaurant.html", args)

# Delete product
def deleteRestaurantProductView(request, shop_id, id):
    cart1 = request.session.get("cart1", None)
    shopId = Shop.objects.get(pk=shop_id)
    product_id = str(id)

    if request.method == "POST":
        if cart1:
            cart1.pop(product_id)

            request.session["cart1"] = cart1
            # print(cart1)
        return redirect(f"/restaurant/open-restaurant/{shop_id}/")


def restaurantAllPaymentsView(request, shop_id):
    shopId = get_object_or_404(Shop, pk=shop_id)
    if shopId.user == request.user:

        print(f"{shopId=}")
        orders = RestCheckout.objects.filter(shop=shopId)
        
        args = {
            "orders": orders,
            "shopId": shopId,
        }
        return render(request, "restaurant/restaurantAllPayments.html", args)

    else:
        return redirect("warning")


def restaurantOrderDetailsView(request, shop_id, id):
    shopId = get_object_or_404(Shop, id=shop_id)
    order_details = RestCheckout.objects.get(id=id)

    args = {
        "order_details": order_details,
        "shopId": shopId,
    }
    return render(request, "restaurant/orderDetails.html", args)


# restaurant receipt
def restaurantReceiptView(request, shop_id, id):
    shopId = get_object_or_404(Shop, id=shop_id)
    order_details = RestCheckout.objects.get(id=id)

    total_item = 0
    
    for item in order_details.items.all():
        total_item += item.quantity

    args = {
        "order_details": order_details,
        "total_item": total_item,
        "shopId": shopId,
    }
    return render(request, "restaurant/restaurantReceipt.html", args)


# selecting the customer or walkin

def select_customer_or_walkin(request, id):
    get_customerId = Customer.objects.get(pk=id)
    
    args = {
        "get_customerId": get_customerId
    }
    return render(request, "restaurant/openRestaurant.html", args)


def get_table_page(request, shop_id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)
    if shopId.user == request.user:
        tables = Table.objects.filter(
            is_active = True
        )
        args = {
            "shopId": shopId,
            "tables": tables,
        }
        return render(request, "restaurant/availableTable.html", args)
    else:
        return redirect("warning")

def get_table_details(request, shop_id, id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)
    if shopId.user == request.user:
        table_id = Table.objects.get(pk=id)
        category = Category.objects.filter(
                shop=shopId
            )
        items = Item.objects.filter(
                Q(out_of_stock=False) and Q(shop=shopId)
            )
        cart2 = request.session.get("cart2")
        remove = request.POST.get('remove')
        item_id = request.POST.get("item_id")

        ## Getting all customer

        customers = Customer.objects.filter(
            added_by=request.user
        )

        if item_id is not None:
            if cart2:
                quantity = cart2.get(item_id)
                if quantity:
                    if remove:
                        cart2[item_id] = quantity - 1
                    else:
                        cart2[item_id] = quantity + 1
                else:
                    cart2[item_id] = 1
                if cart2[item_id] < 1:
                    cart2.pop(item_id)
            else:
                cart2 = {}
                cart2[item_id] = 1

            request.session['cart2'] = cart2

            return redirect(f"/restaurant/table-details/{shop_id}/{table_id.id}/")
        
        # Getting All cart products

        if not cart2:
            request.session.cart2 = {}

        cart_products2 = None
        
        if cart2:
            ids = list(request.session.get('cart2').keys())
            print(f"{ids=}")
            cart_products2 = Item.get_items(ids)



        args = {
            "table_id": table_id,
            "category": category,
            "items": items,
            "cart_products2": cart_products2,
            "shopId": shopId,
        }
        return render(request, "table/table_cart.html", args)
    else:
        return redirect("warning")


def table_checkout_validation(request, id, shop_id, *args, **kwargs):
    cart2 = request.session.get("cart2")
    shopId = Shop.objects.get(pk=shop_id)
    tableId = Table.objects.get(pk=id)
    if request.method == "POST":
        ids = list(request.session.get('cart2').keys())

        if len(ids) <= 0:
            return redirect("open-restaurant")

        cart_products2 = Item.get_items(ids)
        items = cart_products2
        customer_name = request.POST.get("customer_name")
        customer_phone = request.POST.get("customer_phone")
        table = tableId
        amount_received = request.POST.get("amount_received")
        change = request.POST.get("change")
        customerId = request.POST.get("customer_id")
        discount = request.POST.get("discount")
    
        table_checkout = RestCheckout(
            customer_name=customer_name,
            customer_phone=customer_phone,
            table=table,
            table_status="PAID",
            discount=discount,
            amount_received=amount_received,
            change=change,
            shop=shopId,
        )
        table_checkout.save()

        total = 0
        for item in item_item:
            quantity = cart2.get(str(item.id))
            total += item.item_price * quantity
            cartItems = CartItems(
                item=item,
                quantity=quantity
            )
            cartItems.save()
            table_checkout.item_item.add(cartItems)
        
        table_checkout.total = total
        table_checkout.save()
        # Clearing cookie
        cart2 = {}
        request.session["cart1"] = cart2
        return HttpResponse("Success")
        # return redirect(f"/restaurant/restaurant-receipt/{shop_id}/{checkout.id}/")
    args = {
        "tableId": tableId,
    }
    return render(request, "table/table_cart.html", args)


def get_table_orders(request, shop_id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)
    if shopId.user == request.user:
        get_table_orders = TableCheckout.objects.filter(
            shop=shopId
        )
        args = {
            "shopId": shopId,
            "get_table_orders": get_table_orders,
        }
        return render(request, "", args)
    else:
        return redirect("warning")



def get_table_receipt(request, shop_id, id, *args, **kwargs):
    shopId = get_object_or_404(Shop, pk=shop_id)
    if shopId.user == request.user:
        get_receipt = TableCheckout.objects.get(pk=id)
        args = {
            "shopId": shopId,
            "get_receipt": get_receipt,
        }
        return render(request, "", args)
    else:
        return redirect("warning")

def closeRegisterView(request, shop_id):
    shopId = get_object_or_404(Shop, id=shop_id)

    args = {
        "shopId": shopId,
    }
    return render(request, "restaurant/closeRegister.html", args)