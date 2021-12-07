from django.urls import path

from .views import (
    adminpanelHome, adminpanelOrder,
    departmentHomeView, editDepartmentView, createDepartmentView,
    createItemDepartmentView, createDepartmentCategory,
    categoryHomeView, editCategoryView, createCategoryView, createCategoryItemView,
    adminDeleteCategoryiew, adminEditCategoryView,
    productHomeView, editProducteView, createProducteView,
    customerHomeView, editCustomerView, personalCustomerView, businessCustomerView,
    vendorView, editVendorView,createVendorView,
    employeeView,editEmployeeView,createEmployeeView,
    contactView, login_for_admin, logoutView,
    successView, failedView, notFoundView, warningView,

)

urlpatterns = [

    # Login For Admin of the shop owner
    path("login/", login_for_admin, name="login_for_admin"),
    # Logout For Admin of the shop owner
    path("logout/", logoutView, name="logoutView"),

    path("home/<int:shop_id>/", adminpanelHome, name="admin-home"),
    path("orders/<int:shop_id>/", adminpanelOrder, name="admin-order"),

    # Department
    path("department/<int:shop_id>/", departmentHomeView, name="department"),
    path("edit-department/", editDepartmentView, name="edit-department"),
    path("create-department/", createDepartmentView, name="create-department"),
    path("create-item/", createItemDepartmentView, name="create-item"),
    path("create-department-category/", createDepartmentCategory,
         name="create-department-category"),

    # Category
    path("category/<int:shop_id>/", categoryHomeView, name="category"),
    path("edit-category/<int:shop_id>/<int:cat_id>/", editCategoryView, name="edit-category"),
    path("create-category/<int:shop_id>/", createCategoryView, name="create-category"),
    path("create-category-item/", createCategoryItemView,
         name="create-category-item"),

    # Category form
    path("admin-delete-category/<int:shop_id>/<int:cat_id>/", adminDeleteCategoryiew, name="admin-delete-category"),
    path("admin-edit-category/<int:shop_id>/<int:cat_id>/", adminEditCategoryView, name="admin-edit-category"),

    # Product
    path("product/<int:shop_id>/", productHomeView, name="product"),
    path("edit-product/<int:id>/", editProducteView, name="edit-product"),
    path("create-product/<int:shop_id>/", createProducteView, name="create-product"),


    # customer
    path("customer/<int:shop_id>/", customerHomeView, name="customer"),
    path("edit-customer/", editCustomerView, name="edit-customer"),
    path("personal-customer/", personalCustomerView, name="personal-customer"),
    path("business-customer/", businessCustomerView, name="business-customer"),

    # vendor
    path("vendor/<int:shop_id>/", vendorView, name="vendor"),
    path("edit-vendor/", editVendorView, name="edit-vendor"),
    path("create-vendor/<shop_id>/", createVendorView, name="create-vendor"),

    # employee
    path("employee/", employeeView, name="employee"),
    path("edit-employee/", editEmployeeView, name="edit-employee"),
    path("create-employee/", createEmployeeView, name="create-employee"),


    # settings
        path("contact/", contactView, name="contact"),

    # Exception
    # success
    path("success/", successView, name="success"),  

    # failed  
    path("failed/", failedView, name="failed"),
    # not found  
    path("notFound/", notFoundView, name="notFound"),
     # warning  
    path("warning/", warningView, name="warning"),




]
