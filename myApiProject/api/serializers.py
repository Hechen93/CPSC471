from rest_framework import serializers
from . import models

class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderHistory
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['id','customer','addressLine1','addressLine2','city','province','postcode','country']

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = ['id','name','customerAddress','customerOrderHistory']
        depth = 1

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = ['id','cart','paymentType','paymentAmount']

    def validate_cart(self,value):
        if(value.paymentDone == True):
            raise serializers.ValidationError("Payment has already been done!")
        if(value.totalCost == 0.0):
            raise serializers.ValidationError("There is no payment to be made!")
        return value

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id','name','colour','size','unitPrice','categoryID']
        
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['id','cart','product','quantity','line_total']
    

    def validate(self, data):
        if(data['product'].productInventory.quantity < data['quantity']):
            raise serializers.ValidationError("Not Enough Inventory")
        if(data['cart'].paymentDone == True):
            raise serializers.ValidationError("Payment has been made, cannnot modify cart")
        return data

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id','customer','totalCost','paymentDone']

    def validate_paymentDone(self, value):
        if(value == True):
            raise serializers.ValidationError("Payment has been done, cannot modify cart")
        return value

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shipment
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Warehouse
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Supplier
        fields = '__all__'


