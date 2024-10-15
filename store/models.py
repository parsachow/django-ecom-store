from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

STATUS = (
    ("OA", "Order Accepted"),
    ("OC", "Order Canceled"),
    ("OBP", "Order Being Processed"), 
    ("OFD", "Out For Delivery"), 
    ("OID", "Order Is Delivered")
    )

# Create your models here. 

class Category(models.Model):
    product_type = models.CharField(max_length=50)
    
    def __str__(self):
        return self.product_type
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'category_id': self.id})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=350, blank=True, null=True)
    color = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True) 
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_id': self.id})



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS, default=STATUS[0][0])
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Shipment Status - {self.get_status_display()}"
    
    def get_total_price(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_item_price()
        return total
    
    class Meta:
        ordering = ['-ordered_at']


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.product.name
        
    def get_item_price(self):
        total = self.product.price * self.quantity
        return total




# -----------


# class Customer(models.Model):
#     user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
    
#     def __str__(self):
#         return self.name

#using post_save signal to associate User to Customer    

# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)
#         print("customer created")
# post_save.connect(create_customer, sender=User)

# # @receiver(post_save, sender=User)
# def save_customer(sender, instance, **kwargs):
#     instance.customer.save()
   