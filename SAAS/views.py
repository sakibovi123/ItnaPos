from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Package, PackageCheckout, Shop
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your views here.

# landing

def saasHome(request):
    packages = Package.objects.all()[:3]

    args = {
        "packages": packages,
    }
    return render(request, "landing/landing.html", args)

@login_required(login_url='/login/')
def packageDetails(request, id):
    package_obj = get_object_or_404(Package, id=id)

    # print("User:", request.user)

    package_checkout_obj = PackageCheckout.objects.filter(customer_obj=request.user, is_expired=False)

    # print("PACKAGE CHECKOUT:", package_checkout_obj)
    if package_checkout_obj.exists():
        package_checkout_obj = package_checkout_obj.last()
        return redirect(f"/user-package/{package_checkout_obj.id}")

    args = {
        "package_obj": package_obj,
    }
    return render(request, "package/packageDetails.html", args)

@login_required(login_url='/login/')
def packageCheckout(request, id):
    package_obj = get_object_or_404(Package, id=id)

    if request.method == "POST":
        customer_name = request.POST.get("cust_name")
        customer_contact = request.POST.get("cust_contact")
        shop_name = request.POST.get("shop_name")
        shop_logo_img = request.FILES.get("shop_logo")
        bkash_number = request.POST.get("user_bkash_number")
        bkash_trx = request.POST.get("user_bkash_trans_id")
        nagad_number = request.POST.get("user_nagad_number")
        nagad_trx = request.POST.get("user_nagad_trans_id")

        # print(shop_name)

        shop_obj = Shop.objects.filter(shop_name=shop_name)
        print(shop_obj)
        user_exist = PackageCheckout.objects.filter(customer_obj=request.user)

        if shop_obj.exists():
            messages.error(request, "Shop with this name already exists!")
            return redirect(f"/package-details/{id}/")

        if user_exist.exists():
            messages.error(request, "Email is already being used! Please create a new account...")
            return redirect(f"/package-details/{id}/")

        if package_obj and customer_name and customer_contact and shop_name and shop_logo_img:
            if len(bkash_number) <= 0 and len(nagad_number) <= 0:
                messages.error(request, "You have to pay via bKash or Nagad!")
                return redirect(f"/package-details/{id}/")
            else:
                # For bKash
                if len(bkash_number) > 0:
                    if len(bkash_trx) > 0:
                        shop_obj = Shop(user=request.user, shop_name=shop_name, shop_logo=shop_logo_img)
                        shop_obj.save()

                        package_checkout_obj = PackageCheckout(
                            customer_obj=request.user,
                            customer_name=customer_name,
                            customer_phone_number=customer_contact,
                            shop=shop_obj,
                            package=package_obj,
                            total=package_obj.package_price,
                            bkash_number=bkash_number,
                            bkash_transaction_id=bkash_trx
                        )
                        package_checkout_obj.save()

                        # Pakcage due date
                        package_checkout_obj.due_date = package_checkout_obj.created_at + timedelta(days=package_obj.duration)
                        package_checkout_obj.save()

                        return HttpResponse("OKAY BKASH!")
                    else:
                       messages.error(request, "Please submit bKash transaction ID!")
                       return redirect(f"/package-details/{id}/")
                # For nagad
                elif len(nagad_number) > 0:
                    if len(nagad_trx) > 0:
                        shop_obj = Shop(user=request.user, shop_name=shop_name, shop_logo=shop_logo_img)
                        shop_obj.save()

                        package_checkout_obj = PackageCheckout(
                            customer_obj=request.user,
                            customer_name=customer_name,
                            customer_phone_number=customer_contact,
                            shop=shop_obj,
                            package=package_obj,
                            total=package_obj.package_price,
                            nagad_number=nagad_number,
                            nagad_transaction_id=nagad_trx
                        )
                        package_checkout_obj.save()

                        return HttpResponse("OKAY NAGAD!")
                    else:
                        messages.error(request, "Please submit Nagad transaction ID!")
                        return redirect(f"/package-details/{id}/")

@login_required(login_url='/login/')
def userPackageView(request, id):
    package_checkout_obj = get_object_or_404(PackageCheckout, id=id)

    today_date = datetime.now() - timedelta(days=1)
    today_date = datetime.strftime(today_date, "%Y-%m-%d %H:%M:%S")
    today_date = datetime.strptime(today_date, "%Y-%m-%d %H:%M:%S")

    package_expired_date = package_checkout_obj.due_date
    package_expired_date = datetime.strftime(package_expired_date, "%Y-%m-%d %H:%M:%S")
    package_expired_date = datetime.strptime(package_expired_date, "%Y-%m-%d %H:%M:%S")

    print(today_date)
    print(package_expired_date)

    if today_date > package_expired_date:
        package_checkout_obj.is_expired = True
        package_shop = package_checkout_obj.shop

        shop_obj = get_object_or_404(Shop, id=package_shop.id)

        shop_obj.is_active = False

        package_checkout_obj.save()
        shop_obj.save()

    args = {
        "package_checkout_obj": package_checkout_obj,
    }
    return render(request, "package/userPackage.html", args)

# log in and registration
def logInView(request):
    packages = Package.objects.all()[:3]

    args = {
        "packages": packages,
    }
    return render(request, "account/login.html", args)

def regView(request):
    packages = Package.objects.all()[:3]

    args = {
        "packages": packages,
    }
    return render(request, "account/registration.html", args)   


# footer pages    
# about us
def aboutusView(request):
    args = {}
    return render(request, "footer_pages/aboutus.html", args)  

# support
def supportView(request):
    args = {}
    return render(request, "footer_pages/support.html", args) 
