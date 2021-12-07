from django.urls import path

from .views import (
    openRestaurantView, restaurantDueView, restaurantAvailableTableView,addingNewCustomer,get_checkout,
    deleteRestaurantProductView, restaurantAllPaymentsView, restaurantOrderDetailsView,
    restaurantReceiptView, select_customer_or_walkin, get_table_page, get_table_details, get_table_orders, get_table_receipt,
    closeRegisterView, table_checkout_validation
)

urlpatterns = [
    path("open-restaurant/<int:shop_id>/", openRestaurantView, name="open-restaurant"),
    path("due-restaurant/<int:shop_id>/", restaurantDueView, name="due-restaurant"),
    path("<int:shop_id>/available-tables/", restaurantAvailableTableView, name="available-tables"),
    path("delete-product/<int:shop_id>/<int:id>/", deleteRestaurantProductView, name="delete-product"),
    path("all-payments/<int:shop_id>/", restaurantAllPaymentsView, name="restaurant-all-payments"),
    path("order-details/<int:shop_id>/<int:id>/", restaurantOrderDetailsView, name="restaurant-order-details"),

    ## adding Customer URl
    path("adding-customer/<int:shop_id>/", addingNewCustomer, name="addingNewCustomer"),

    # Checkout
    path("checkout/<int:shop_id>/", get_checkout, name="get_checkout"),

    # restaurant receipt
    path("restaurant-receipt/<int:shop_id>/<int:id>/", restaurantReceiptView, name="restaurant-receipt"),

    # Getting Customer iD to save 

    path("<int:id>/", select_customer_or_walkin, name="SelectCustomer"),

    # Getting Table Page URL
    path("tables/<int:shop_id>/", get_table_page, name="get_table_page"),
    # Getting Table Details Page URL
    path("table-details/<int:shop_id>/<int:id>/", get_table_details, name="TableDetails"),
    # Getting all table orders url
    path("table-orders/<int:shop_id>/", get_table_orders, name="get_table_orders"),
    # Getting table receipt
    path("table-order-details/<int:shop_id>/<int:id>/", get_table_receipt, name="get_table_receipt"),
    # close register
    path("close-register/<int:shop_id>/", closeRegisterView, name="close-register"),
    # table checkout validation
    path("validation/<int:id>/<int:shop_id>/", table_checkout_validation, name="table_checkout_validation"),
]