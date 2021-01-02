from django.urls import path,include
from . import views
from rest_framework.authtoken import views as authviews
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('customers/', views.CustomerList.as_view()),
    path('customers/<int:pk>/', views.CustomerDetail.as_view()),

    path('payments/', views.PaymentList.as_view()),
    path('payments/<int:pk>/', views.PaymentDetail.as_view()),

    path('carts/', views.CartList.as_view()),
    path('carts/<int:pk>/', views.CartDetail.as_view()),

    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),

    path('shipments/', views.ShipmentList.as_view()),
    path('shipments/<int:pk>/', views.ShipmentDetail.as_view()),

    path('warehouses/', views.WarehouseList.as_view()),
    path('warehouses/<int:pk>/', views.WarehouseDetail.as_view()),

    path('suppliers/', views.SupplierList.as_view()),
    path('suppliers/<int:pk>/', views.SupplierDetail.as_view()),

    path('inventorys/', views.InventoryList.as_view()),
    path('inventorys/<int:pk>/', views.InventoryDetail.as_view()),

    path('orderHistorys/<int:customer>/', views.OrderHistoryList.as_view()),
    path('orderHistorys/<int:customer>/<int:orderID>', views.OrderHistoryDetail.as_view()),

    path('cartItems/<int:cart>/', views.CartItemList.as_view()),
    path('cartItems/<int:cart>/<int:pk>/', views.CartItemDetail.as_view()),

    path('addresses/', views.AddressList.as_view()),
    path('addresses/<int:customer>/', views.AddressDetail.as_view()),

    path('api-token-auth/', authviews.obtain_auth_token, name="api-token-auth"), 
]
