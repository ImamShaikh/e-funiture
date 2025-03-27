from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    price = models.IntegerField()
    category = models.CharField(max_length=255)
    desc = models.TextField()
    specification = models.TextField()

    def _str_ (self):
        return self.name
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
class cart(models.Model):
    user = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE,null=True, blank=True)
    product = models.ManyToManyField(to=products, related_name='cart_products', blank=True)
    
    def _str_ (self):
        return self.user.first_name
    
class Order(models.Model):
    order_id = models.CharField(max_length=50) # to identify order group
    user = models.ForeignKey(User, related_name='order_customer', on_delete=models.CASCADE)
    product = models.ForeignKey(products, related_name='order_item', on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=10)
    date = models.DateTimeField(default=datetime.now())
    STATUS_CHOICES = [('Pending', 'Pending'), ('Delivered', 'Delivered'), ('On the Way', 'On the way')]
    status = models.CharField(max_length=50, choices= STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.product.name} - {self.user.first_name}'
    
class contact ( models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=False)
    text = models.TextField()

    def __str__(self):
        return f'sender name is {self.first_name} {self.last_name}'