from django.db import models
from decimal import Decimal
from django.db.models import F, Sum
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from datetime import datetime 

# Create your models here.
class Product(models.Model):
    class ProcutTypes(models.IntegerChoices):
        SHIRTS = 1
        PANTS = 2
        DRESSES = 3
        BRAS = 4
        JACKETS = 5
        SHORTS = 6

    SIZES = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
        ('XXXL', 'Extra Extra Extra Large'),
    )
    name = models.CharField(max_length=250, unique=True)
    colour = models.CharField(max_length=50)
    size = models.CharField(max_length=4, choices=SIZES)
    unitPrice = models.FloatField()
    categoryID = models.IntegerField(choices=ProcutTypes.choices)

    class Meta:
        app_label='api'

    def __str__(self):
        return self.name

    def getPrice(self):
        self.unitPrice

class Customer(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label='api'

    def __str__(self):
        return self.name

class Address(models.Model):
    customer = models.ForeignKey('Customer',related_name='customerAddress', on_delete=models.CASCADE, null=False)
    addressLine1 = models.CharField(max_length=250)
    addressLine2 = models.CharField(max_length=250, null=True, blank=True)
    province = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    class Meta:
        app_label='api'

    def __str__(self):
        return self.addressLine1

class Warehouse(models.Model):
    city = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label='api'

    def __str__(self):
        return self.city

class Inventory(models.Model):
    product = models.OneToOneField('Product', related_name='productInventory', primary_key=True, on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', related_name='warehouseInventory', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        app_label='api'

    def __str__(self):
        return str(self.product)

class Supplier(models.Model):
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)

    class Meta:
        app_label='api'

    def __str__(self):
        return self.company

class Shipment(models.Model):
    payment = models.ForeignKey('Payment', related_name='shipmentPayment',on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', related_name='shipmentCart',on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', related_name='shipmentWarehouse', on_delete=models.CASCADE)
    orderDate = models.DateField(auto_now_add=True, blank=True)
    shipDate = models.DateField(auto_now_add=True, blank=True)

    class Meta:
        app_label='api'

    def __str__(self):
        return str(self.orderDate)

class OrderHistory(models.Model):
    customer = models.ForeignKey('Customer', related_name='customerOrderHistory',on_delete=models.CASCADE)
    orderID = models.ForeignKey('Shipment', related_name='shipmentOrderID', on_delete=models.CASCADE)

    class Meta:
        unique_together = (["customer","orderID"])
        app_label='api'

    def __str__(self):
        return str(self.customer)

class Cart(models.Model):
    customer = models.ForeignKey('Customer',related_name='cartCustomer', on_delete=models.CASCADE)
    totalCost = models.FloatField(default=0.0)
    paymentDone = models.BooleanField(default=False)

    def total_cost(self):
        cartItems = CartItem.objects.all()
        sum = 0
        for c in cartItems:
            if str(c.cart) == str(self.id):
                sum = sum + c.line_total
        self.totalCost = sum
        self.save()
        return sum

    class Meta:
        app_label = 'api'
    
    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', related_name='ciCart',on_delete=models.CASCADE, null=False, blank = False)
    product = models.ForeignKey('Product',related_name='cartItemProduct', on_delete=models.CASCADE)
    lineTotal = models.DecimalField(decimal_places=2, max_digits=10, default=0.0, null = True, blank = True)
    quantity = models.IntegerField(default=1)
    
    @property
    def line_total(self):
        self.lineTotal = self.quantity * self.product.unitPrice 
        return self.quantity * self.product.unitPrice

    class Meta:
        app_label = 'api'
    
    def __str__(self):
        return str(self.id)

class Payment(models.Model):
    PAYMENT_TYPES = (
        ('CC', 'Credit Card'),
        ('DC', 'Debit Card'),
        ('COD', 'Cash On Delivery'),
    )

    cart = models.ForeignKey('Cart',related_name='paymentCart', on_delete=models.CASCADE, null=False)
    paymentType = models.CharField(max_length=50, choices=PAYMENT_TYPES)

    @property
    def paymentAmount(self):
        return self.cart.total_cost

    class Meta:
        app_label='api'

    def __str__(self):
        return str(self.id)

@receiver(post_save, sender=CartItem, dispatch_uid="decrease_stock_count")
def decrese_stock(sender, instance, **kwargs):
    instance.product.productInventory.quantity = instance.product.productInventory.quantity - instance.quantity
    instance.product.productInventory.save()

@receiver(post_delete, sender=CartItem, dispatch_uid="increase_stock_count")
def increase_stock(sender, instance, **kwargs):
    instance.product.productInventory.quantity = instance.product.productInventory.quantity + instance.quantity
    instance.product.productInventory.save()

@receiver(post_save, sender=Payment, dispatch_uid="add_shipment")
def add_shipment(sender, instance, **kwargs):
    cartItems = CartItem.objects.filter(cart=instance.cart)
    instance.cart.paymentDone = True
    instance.cart.save()
    for c in cartItems:
        order = Shipment.objects.create(payment=instance, cart=instance.cart, warehouse=c.product.productInventory.warehouse)
        orderHistory = OrderHistory.objects.create(customer=instance.cart.customer, orderID=order)
        order.save()
        orderHistory.save()
    
