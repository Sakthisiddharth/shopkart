from django.urls import path
from . import views


urlpatterns = [
path('', views.home, name='home'),
path('product/<int:id>/', views.product_detail, name='product_detail'),
# path('carts/', views.cart, name='cart'),
path('checkout/', views.checkout, name='checkout'),
path('buy-now/<int:product_id>/', views.product_buy_now, name='product_buy_now'),   
path('order-success/', views.order_success, name='order_success'),
path('search/', views.search_products, name='search'),

path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
path('cart/', views.cart_view, name='cart'),
path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
path('dummy/<int:id>/',views.dummy_buy, name='dummy'),
path('orders/', views.order_status, name='order_status'),
path('about/', views.about, name='about'),
]