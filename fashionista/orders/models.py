import datetime
import math
import django
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import Avg, Sum, Count
from django.db.models.signals import post_save, pre_save
from django.utils import timezone

Cart=apps.get_model('carts','Cart',require_ready=False)
User=settings.AUTH_USER_MODEL

STATUS =(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shipped'),
    ('refunded','Refunded')
)

class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated", "-timestamp")

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

class Order(models.Model):
    billing_profile =models.ForeignKey('orders.BillingProfile',on_delete=models.CASCADE,null=True,blank=True)
    ordered =models.CharField(default='True', max_length=10)
    shipping_address=models.ForeignKey('addresses.Address',related_name="shipping",on_delete=models.CASCADE,blank=True,null=True)
    billing_address=models.ForeignKey('addresses.Address',related_name="billing",on_delete=models.CASCADE,blank=True,null=True)
    status = models.CharField(choices=STATUS,default='created',max_length=20)
    shipping_total =models.DecimalField(max_digits=100, default=20,decimal_places=2)
    finaltotal = models.DecimalField(default=0.00, max_digits=30, decimal_places=2)
    cart = models.ForeignKey('carts.Cart',on_delete=models.CASCADE)
    active =models.BooleanField(default=True)
    updated=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    confirm=models.BooleanField()

    objects=OrderManager()

    def __str__(self):
        return str(self.id)

    def get_items(self):
        items=self.cart.items.all()
        return items

    #check whether all the required fields got its value or not
    def check_done(self):
        billing_profile=self.billing_profile
        shipping_address=self.shipping_address
        billing_address=self.billing_address
        finaltotal=self.finaltotal
        confirm=self.confirm

        if billing_profile and billing_address and shipping_address and finaltotal and confirm >0:
            return True
        else:
            return False

    #update product count in Product table only if order is confirm
    def mark_done(self):
        if self.check_done():
            items=self.cart.items.all()
            for i in items:
                product=i.product
                quantity=i.quantity
                project_object=apps.get_model('products.Product').objects.get(id=product.id)
                project_object.quantity=project_object.quantity-quantity
                project_object.save()

            self.status='created'
            self.save()
        return self.status

    #update order total with additional costs
    def update_total(self):
        cart_total = self.cart.finaltotal
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.finaltotal = formatted_total
        self.save()
        return new_total


def post_save_order_finaltotal(sender,instance,created,*args,**kwargs):
    if not created:
        order = instance
        time = timezone.now()
        cart_finaltotal = order.cart.finaltotal
        order_shipping = order.shipping_total
        order.updated = time
        new_total = cart_finaltotal + order_shipping
        order.finaltotal = new_total

    if created:
        instance.update_total()


post_save.connect(post_save_order_finaltotal,sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.finaltotal
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

#After creating order, update the total (shipping+card_total)
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)

#It is nothing but the profile of user who places order (whether it is admin,employee or customer)
class BillingProfile(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance)

#whenever theres a new admin or employee at that time billing profile gets created
post_save.connect(user_created_receiver,sender=User)