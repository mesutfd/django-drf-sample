from django.urls import include, path
from rest_framework_nested import routers

from . import views

# router = SimpleRouter()

# this will provide some extra features like: /product.json etc.
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')
# urlpatterns = router.urls

# lookup field will make a product_pk parameter in our url
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('cart-items', views.CartViewSet, basename='cart-items')

# in case you want to have some customized paths
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
