from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .filters import ProductFilter
from .models import Product, Collection, OrderItem, Review, Cart
from .pagination import DefaultPagination
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs.get('product_pk'),
        }

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']).prefetch_related('product')


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # filtering by third-party application: django-filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    # filter_fields = ['collection_id']

    # pagination_class = PageNumberPagination
    pagination_class = DefaultPagination

    serializer_class = ProductSerializer
    lookup_field = 'pk'  # name of the url parameter
    lookup_url_kwarg = 'pk'

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product can not be deleted because it is associated with an order item'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # manual filtering
    # def get_queryset(self):
    #
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id:
    #         return Product.objects.filter(collection_id=collection_id)
    #
    #     return Product.objects.all()


class CollectionViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.annotate(products_count=Count('products')).all()

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection can not be deleted because it is associated one or more products'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {
            'request': self.request
        }

# class ProductList(ListCreateAPIView):
#     pass
#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()
#
#     def get_serializer_class(self):
#         return ProductSerializer
#
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         # pass queryset or model to serializer class to serialize, and data=request.data to deserialize
#         serializer = ProductSerializer(data=request.data)
#
#         # raise_exception kwarg will save the code from if, else expression
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Ok')


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
#     if request.method == 'GET':
#         # product = Product.objects.get(pk=id)
#         serializer = CollectionSerializer(collection, context={'request': request})
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     elif request.method == 'PATCH':
#         serializer = CollectionSerializer(collection, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection can not be deleted because it contains one or more products'})
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductDetail(APIView):
#
#     def get(self, request, id):
#         # product = Product.objects.get(pk=id)
#         product = get_object_or_404(Product, pk=id)
#         if not product:
#             return Response(status=status.HTTP_404_NOT_FOUND,
#                             data={'error': 'Product with given id was not found in database'})
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def patch(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product can not be deleted because it is associated with an order item'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == "GET":
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == "POST":
#         # pass queryset or model to serializer class to serialize, and data=request.data to deserialize
#         serializer = ProductSerializer(data=request.data)
#
#         # raise_exception kwarg will save the code from if, else expression
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Ok')


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         # product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     elif request.method == 'PATCH':
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product can not be deleted because it is associated with an order item'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == "GET":
#         # queryset = Collection.objects.select_related('featured_product').all()
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#
#     elif request.method == "POST":
#         # pass queryset or model to serializer class to serialize, and data=request.data to deserialize
#         serializer = CollectionSerializer(data=request.data)
#
#         # raise_exception kwarg will save the code from if, else expression
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('Ok')
