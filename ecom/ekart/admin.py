from django.contrib import admin
from .models import products, cart, Order, contact

# Register your models here.
admin.site.register(products)
admin.site.register(cart)
admin.site.register(Order)
admin.site.register(contact)