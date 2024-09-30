from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login_view,name='login'),
    path('usignup',views.signup,name='signup'),
    path('ssignup', views.ssignup, name='ssignup'),
    path('signout',views.signout,name='signout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('seller',views.seller,name='seller'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'),
    path('privacy',views.privacy,name='privacy'),
    path('condition',views.condition,name='condition'),
    path('my_products',views.my_products,name='my_products'),
    path('product/update/<int:pk>/', views.update_product, name='update_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('products/', views.product_list, name='product_list'),
    path('products/category/<int:category_id>/', views.product_list, name='product_list_by_category'),
    path('products/buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('customer_support',views.customer_support,name='customer_support'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)