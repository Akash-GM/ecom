from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "stock")

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Come again with a real price")
        return value


class OrderItemSeralizer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # incase you wanna display all details of the product above line

    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )

    # for specific fields above lines

    # remove all above lines if you only want to see the product pk

    class Meta:
        model = OrderItem
        fields = ("product_name", "product_price", "quantity", "item_subtotal")
        # product is a foreign key here
        # item_subtotal is an @property in the model OrderItem


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSeralizer(many=True, read_only=True)
    # if you comment the above line you will get the primary keys only of items

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = ("order_id", "created_At", "user", "status", "items", "total_price")
        # user is a foreign key here


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
