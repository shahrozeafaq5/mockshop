from django.contrib import admin
from django.urls import path
from shop import views as shop_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shop_views.product_list, name='home'),
    path('products/', shop_views.product_list, name='product_list'),
    path('products/<int:product_id>/', shop_views.product_detail, name='product_detail'),
    path('cart/', shop_views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', shop_views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', shop_views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', shop_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', shop_views.checkout, name='checkout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
