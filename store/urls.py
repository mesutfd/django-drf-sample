from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# router = SimpleRouter()

# this will provide some features like: /product.json etc.
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# urlpatterns = router.urls

# in case you want to have some customized paths
urlpatterns = [
    path('', include(router.urls)),
]
