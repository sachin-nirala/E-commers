from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('product', views.product, name='product'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('category/<str:pk>', views.category, name='category'),
    path('add-to-cart/<str:pk>', views.add_to_cart, name='add'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('results', views.search_results, name='results'),

]
