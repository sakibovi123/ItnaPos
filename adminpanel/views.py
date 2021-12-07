from django.shortcuts import get_object_or_404, render, redirect
from restaurant.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse




def login_for_admin(request):
    # shop_id = get_object_or_404(Shop, pk=shop_id)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_authenticated:
            # print(user.id)
                print(user)
                shop_id = get_object_or_404(Shop, user=user)
                print(shop_id)
                login(request, user)
                return redirect(f"/adminpanel/home/{shop_id.id}/")
            else:
                return HttpResponse("Something Went Wrong")
    args = {}
    return render(request, "account/admin_login.html", args)


def logoutView(request):
    # shop_id = get_object_or_404(Shop, pk=shop_id)
    logout(request)
    return redirect("login_for_admin")



@login_required(login_url="login_for_admin")
def adminpanelHome(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:
        args = {
            "shop_id": shop_id,
        }
        return render(request, "adminpanel/admin-panel.html", args)
    else:
        return HttpResponse("You are not the owner of this shop")


@login_required(login_url="login_for_admin")
def adminpanelOrder(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:
        orders = RestCheckout.objects.filter(
            shop=shop_id
        )
        args = {
            "orders": orders,
            "shop_id": shop_id,
        }
        return render(request, "adminpanel/orders.html", args)
    else:
        return HttpResponse("You are not the owner of this shop")

# Department
def departmentHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:
        args = {
            "shop_id": shop_id
        }
        return render(request, "department/department.html", args)
    else:
        return HttpResponse("You are not the owner of this shop")

def createDepartmentCategory(request):
    args = {

    }
    return render(request, "department/new-category.html", args)

def editDepartmentView(request):
    args = {

    }
    return render(request, "department/edit-department.html", args)

def createDepartmentView(request):
    args = {

    }
    return render(request, "department/new-department.html", args)

def createItemDepartmentView(request):
    args = {

    }
    return render(request, "department/new-item.html", args)

# Category
def categoryHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:
        category = Category.objects.filter(
            shop=shop_id,
        )
        args = {
            "shop_id": shop_id,
            "category": category,
        }
        return render(request, "category/category.html", args)
    else:
        return HttResponse("You are not the owner of this shop")


def editCategoryView(request, shop_id, cat_id):
    user_shops = Shop.objects.filter(user=request.user, is_active=True)
    shop_id = get_object_or_404(Shop, id=shop_id)
    category_obj = get_object_or_404(Category, pk=cat_id)

    args = {
        "shop_id": shop_id,
        "user_shops": user_shops,
        "category_obj": category_obj
    }
    return render(request, "category/edit-category.html", args)

def adminEditCategoryView(request, shop_id, cat_id):
    cat_obj = get_object_or_404(Category, id=cat_id)
    shop_obj = get_object_or_404(Shop, id=shop_id)

    # print("SHOP Name:", shop_obj.shop_name)

    if request.method == "POST":
        cat_name = request.POST.get("category_name")

        if cat_name:
            cat_obj.category_name = cat_name
            cat_obj.shop = shop_obj

            cat_obj.save()

            return redirect(f"/adminpanel/category/{shop_id}/")
        else:
            return redirect(f"/adminpanel/edit-category/{shop_id}/{cat_id}/")

        



def createCategoryView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:

        shops = Shop.objects.filter(
            user=request.user
        )

        if request.method == "POST":
            category_name = request.POST.get("category_name")
            shop = request.POST.get("shop")

            category = Category(
                category_name=category_name,
                shop=Shop.objects.get(id=shop_id.id)
            )

            category.save()

            return redirect(f"/adminpanel/category/{shop_id.id}/")
        # else:
        #     return HttpResponse("Failed! Please Contact With The Support!")

        args = {
            "shop_id": shop_id,
            "shops": shops
        }
        return render(request, "category/new-category.html", args)
    else:
        return Response("Sorry You are not the owner of this shop")

def adminDeleteCategoryiew(request, shop_id, cat_id):
    category_obj = get_object_or_404(Category, id=cat_id)

    # print(category_obj)
    
    category_obj.delete()
    return redirect(f"/adminpanel/category/{shop_id}/")
        

def createCategoryItemView(request):
    args = {

    }
    return render(request, "category/new-category-item.html", args)

# Product
def productHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:

        products = Item.objects.filter(
            shop=shop_id
        )

        args = {
            "shop_id": shop_id,
            "products": products,
        }
        return render(request, "product/product.html", args)

    else:
        return HttpResponse("You are not the owner of this shop")

def editProducteView(request):
    args = {

    }
    return render(request, "product/edit-product.html", args)

def createProducteView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:

        brands = Brand.objects.all()
        category = Category.objects.filter(shop=shop_id)
        vendors = Vendor.objects.filter(
            shop=shop_id
        )

        if request.method == "POST":
            item_name = request.POST.get("item_name")
            item_price = request.POST.get("item_price")
            buying_price = request.POST.get("buying_price")
            brand = request.POST.get("brand")
            cat = request.POST.get("category")
            vendor = request.POST.get("vendor")
            shop = shop_id.id
            stock_amount = request.POST.get("stock_amount")
            out_of_stock = request.POST.get("out_of_stock")
            item_img = request.FILES.get("item_img")
            product_descriptions = request.POST.get("product_descriptions")
            upc = request.POST.get("upc")
            sku = request.POST.get("sku")

            product = Item(
                item_name = item_name,
                item_price=item_price,
                buying_price = buying_price,
                brand = Brand.objects.get(brand_name=brand),
                category = Category.objects.get(category_name=cat),
                vendor = Vendor.objects.get(vendor_name=vendor),
                shop = Shop.objects.get(id=shop),
                stock_amount = stock_amount,
                out_of_stock = False,
                item_img = item_img,
                product_descriptions = product_descriptions,
                upc = upc,
                sku = sku,
            )

            product.save()

            return HttpResponse("Success")

        args = {
            "shop_id": shop_id,
            "brands": brands,
            "category": category,
            "vendors": vendors,
        }
        return render(request, "product/new-product.html", args)




# customer
def customerHomeView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:
        customers = Customer.objects.filter(added_by=request.user)
        args = {
            "shop_id": shop_id,
            "customers": customers,
        }
        return render(request, "customers/customer.html", args)
    else:
        return HttpResponse("You are not the owner of this shop")



def editCustomerView(request):
    args = {

    }
    return render(request, "customers/edit-customer.html", args)    

def personalCustomerView(request):
    args = {

    }
    return render(request, "customers/personal-customer.html", args)     

def businessCustomerView(request):
    args = {

    }
    return render(request, "customers/business-customer.html", args)     


# vendor
def vendorView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:

        vendors = Vendor.objects.filter(
            shop=shop_id
        )
        args = {    
            "shop_id": shop_id,
            "vendors": vendors,
        }
        return render(request, "vendor/vendor.html", args)  
    else:
        return HttpResponse("You are not the owner of this shop")


def editVendorView(request):
    args = {

    }   
    return render(request, "vendor/edit-vendor.html", args) 

def createVendorView(request, shop_id):
    shop_id = get_object_or_404(Shop, pk=shop_id)
    if shop_id.user == request.user:
        
        args = {
            "shop_id": shop_id,
        }   
        return render(request, "vendor/create-vendor.html", args)     
    else:
        return HttpResponse("You are not the owner of this shop!")


# employee    
def employeeView(request):
    args = {

    }   
    return render(request, "employee/employee.html", args)

def editEmployeeView(request):
    args = {

    }   
    return render(request, "employee/edit-employee.html", args)  

def createEmployeeView(request):
    args = {

    }   
    return render(request, "employee/create-employee.html", args)       


# contact    

def contactView(request):
    args = {

    }   
    return render(request, "adminpanel/contact.html", args)       


# exceptions
# success
def successView(request):
    args = {

    }
    return render(request, "exceptions/success.html", args)  

# failed
def failedView(request):
    args = {

    }
    return render(request, "exceptions/failed.html", args)   
    
# not found
def notFoundView(request):
    args = {

    }
    return render(request, "exceptions/notFound.html", args)      

 # warning
def warningView(request):
    args = {

    }
    return render(request, "exceptions/warning.html", args)