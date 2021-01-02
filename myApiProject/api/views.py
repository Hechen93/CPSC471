from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from django.contrib.auth.models import User, Group
from .serializers import CustomerSerializer
from .serializers import PaymentSerializer
from .serializers import CartSerializer
from .serializers import CartItemSerializer
from .serializers import ShipmentSerializer
from .serializers import AddressSerializer
from .serializers import WarehouseSerializer
from .serializers import SupplierSerializer
from .serializers import OrderHistorySerializer
from .serializers import InventorySerializer
from .serializers import ProductSerializer
from .models import Product
from .models import Customer
from .models import Payment
from .models import Cart
from .models import CartItem
from .models import Inventory
from .models import Address
from .models import Warehouse
from .models import Supplier
from .models import Shipment
from .models import OrderHistory

@permission_classes((IsAuthenticated,))
class CustomerList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        print(request.user)
        customer = Customer.objects.all()
        serializer = CustomerSerializer (customer, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = CustomerSerializer (data=request.data)
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class CustomerDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        customer = Customer.objects.get (pk=pk)
        serializer = CustomerSerializer(customer)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        customer = Customer.objects.filter(pk=pk).first()
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = Customer.objects.filter (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class CartList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        cart = Cart.objects.all()
        for c in cart:
            c.total_cost()
        serializer = CartSerializer (cart, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = CartSerializer (data=request.data)
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class CartDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        cart = Cart.objects.get (pk=pk)
        cart.total_cost()
        serializer = CartSerializer(cart)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        cart = Cart.objects.filter(pk=pk).first()
        serializer = CartSerializer(cart, data=request.data)
        print(cart)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cart = Cart.objects.filter (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class PaymentList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        payment = Payment.objects.all()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = PaymentSerializer (payment, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class PaymentDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def delete(self, request, pk, format=None):
        payment = Payment.objects.filter (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        payment = Payment.objects.get (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = PaymentSerializer(payment)
        return Response (serializer.data)

@permission_classes((IsAuthenticated,))
class ShipmentList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        shipment = Shipment.objects.all()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = ShipmentSerializer (shipment, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = ShipmentSerializer (data=request.data)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class ShipmentDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        shipment = Shipment.objects.get (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = ShipmentSerializer(shipment)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        shipment = Shipment.objects.filter(pk=pk).first()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = ShipmentSerializer(cart, data=request.data)
        print(shipment)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        shipment = Shipment.objects.filter (pk=pk)
        shipment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class WarehouseList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        warehouse = Warehouse.objects.all()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = WarehouseSerializer (warehouse, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = WarehouseSerializer (data=request.data)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class WarehouseDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        warehouse = Warehouse.objects.get (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = WarehouseSerializer(warehouse)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        warehouse = Warehouse.objects.filter(pk=pk).first()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = WarehouseSerializer(warehouse, data=request.data)
        print(warehouse)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        warehouse = Warehouse.objects.filter (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        warehouse.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class ProductList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer (product, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer (data=request.data)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class ProductDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        product = Product.objects.get (pk=pk)
        serializer = ProductSerializer(product)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        product = Product.objects.filter(pk=pk).first()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = ProductSerializer(product, data=request.data)
        print(product)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = Product.objects.filter (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class CartItemList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, cart, format=None):
        cartK = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer (cartK, many=True)
        return Response (serializer.data)

    def post(self, request, cart, format=None):
        cartItem = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer (data=request.data)
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class CartItemDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, cart, pk, format=None):
        cartItem = CartItem.objects.filter(cart=cart).filter(pk=pk).first()
        serializer = CartItemSerializer(cartItem)
        return Response (serializer.data)

    def put(self, request, cart, pk, format=None):
        cartItem = CartItem.objects.filter(cart=cart).filter(pk=pk).first()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = CartItemSerializer(cartItem, data=request.data)
        print(cartItem)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cart, pk, format=None):
        cartItem = CartItem.objects.filter(cart=cart).filter(pk=pk).first()
        cartItem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class AddressList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        address = Address.objects.all()
        serializer = AddressSerializer (address, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = AddressSerializer (data=request.data)
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class AddressDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, customer, format=None):
        address = Address.objects.get (customer=customer)
        serializer = AddressSerializer(address)
        return Response (serializer.data)

    def put(self, request, customer, format=None):
        address = Address.objects.filter(customer=customer).first()
        serializer = AddressSerializer(address, data=request.data)
        print(address)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer, format=None):
        address = Address.objects.filter (customer=customer)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class InventoryList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        inventory = Inventory.objects.all()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = InventorySerializer (inventory, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = InventorySerializer (data=request.data)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class InventoryDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        inventory = Inventory.objects.get (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = InventorySerializer(inventory)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        inventory = Inventory.objects.filter(pk=pk).first()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = InventorySerializer(inventory, data=request.data)
        print(inventory)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        inventory = Inventory.objects.filter (pk=pk)
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class SupplierList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, format=None):
        supplier = Supplier.objects.all()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = SupplierSerializer (supplier, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = SupplierSerializer (data=request.data)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class SupplierDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        supplier = Supplier.objects.get (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = SupplierSerializer(supplier)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        supplier = Supplier.objects.filter(pk=pk).first()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = SupplierSerializer(supplier, data=request.data)
        print(supplier)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        supplier = Supplier.objects.filter (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes((IsAuthenticated,))
class OrderHistoryList (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, customer, format=None):
        orderHistory = OrderHistory.objects.filter(customer=customer)
        serializer = OrderHistorySerializer (orderHistory, many=True)
        return Response (serializer.data)

    def post(self, request, format=None):
        serializer = OrderHistorySerializer (data=request.data)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        if serializer.is_valid ( ):
            serializer.save ( )
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((IsAuthenticated,))
class OrderHistoryDetail (APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request, pk, format=None):
        orderHistory = OrderHistory.objects.get (pk=pk)
        serializer = OrderHistorySerializer(orderHistory)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        orderHistory = OrderHistory.objects.filter(pk=pk).first()
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        serializer = OrderHistorySerializer(orderHistory, data=request.data)
        print(orderHistory)
        if serializer.is_valid ( ):
            print(request.data)
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        orderHistory = OrderHistory.objects.filter (pk=pk)
        if(request.user.is_superuser == False):
            return Response({'Response':"You don't have permission to access this information"})
        orderHistory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
