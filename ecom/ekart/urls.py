"""
URL configuration for ecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('auth', views.auth, name="auth"),
    path('about', views.about, name="about us"),
    path('contact', views.contacts, name="contact us"),
    path('service', views.service, name="service"),
    path('blog', views.blog, name="blog"),
    path('signup',views.signup,name="signup"),
    path('login',views.signin, name="login"),
    path('add_cart', views.cart_p, name='add_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('orders', views.Orders_p, name='orders'),
    path('delete-cart-item/<int:product_id>', views.delete_cart_item, name='delete-cart-item'),
    path('shop', views.shop, name='shop'),
    path('cart/<int:product_id>',views.add_cart, name='cart'),
]
