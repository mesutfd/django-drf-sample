from decimal import Decimal

from rest_framework import serializers

from store.models import Product, Collection, Review, Cart, CartItem


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    @staticmethod
    def perform_create(validated_data):
        collection_data = validated_data.pop('collection')
        product = Product.objects.create(**validated_data)
        product.collection = collection_data
        product.save()
        return product

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)

    # this product count was working, but was low on performance
    # product_count = serializers.SerializerMethodField(method_name='products_count')
    # def products_count(self, collection: Collection):
    #     return collection.product_set.count()


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

    class Meta:
        model = Product
        # Be aware, Mosh said never use __all__ which is for lazy developers
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    @staticmethod
    def get_total_price(cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    @staticmethod
    def get_total_price(cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    @staticmethod
    def calculate_tax(product: Product):
        return round(product.unit_price * Decimal(1.1), 2)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # collection = CollectionSerializer()

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    # customized validation
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Password do not match')
    #     return data

    # customized create method
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return super().create(validated_data)

    # customized update method
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):
    # 'product.id' was my own creativity :D
    product = serializers.IntegerField(read_only=True, source='product.id')

    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description', 'product']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
